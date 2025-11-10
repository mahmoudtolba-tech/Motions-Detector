"""
Advanced Motion Detector Core Engine
Provides sophisticated motion detection with multiple algorithms and features
"""

import cv2
import numpy as np
from datetime import datetime
from typing import Optional, Tuple, List, Dict
import threading
import queue
import json
from pathlib import Path


class MotionDetectorCore:
    """
    Advanced motion detection engine with multiple detection algorithms
    """

    def __init__(self, config: Dict = None):
        """
        Initialize motion detector with configuration

        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        self.cap = None
        self.is_running = False
        self.motion_detected = False
        self.motion_events = []
        self.current_event_start = None

        # Background subtractor for advanced detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=self.config['detection']['bg_threshold'],
            detectShadows=True
        )

        # Frame buffer for advanced algorithms
        self.frame_buffer = queue.Queue(maxsize=30)
        self.processed_frame = None
        self.lock = threading.Lock()

        # Statistics
        self.stats = {
            'total_detections': 0,
            'total_duration': 0,
            'last_detection': None,
            'fps': 0
        }

    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'camera': {
                'index': 0,
                'width': 640,
                'height': 480,
                'fps': 30
            },
            'detection': {
                'algorithm': 'mog2',  # 'simple', 'mog2', 'knn'
                'sensitivity': 50,
                'min_area': 5000,
                'bg_threshold': 16,
                'blur_kernel': 21,
                'dilation_iterations': 2
            },
            'recording': {
                'enabled': False,
                'codec': 'mp4v',
                'output_dir': 'recordings'
            },
            'notifications': {
                'enabled': False,
                'email': None,
                'cooldown': 60
            }
        }

    def initialize_camera(self, camera_index: int = None) -> bool:
        """
        Initialize camera capture

        Args:
            camera_index: Camera device index (default from config)

        Returns:
            bool: Success status
        """
        try:
            index = camera_index if camera_index is not None else self.config['camera']['index']
            self.cap = cv2.VideoCapture(index)

            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera']['width'])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera']['height'])
            self.cap.set(cv2.CAP_PROP_FPS, self.config['camera']['fps'])

            if not self.cap.isOpened():
                return False

            return True
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False

    def detect_motion_simple(self, frame: np.ndarray, prev_frame: np.ndarray) -> Tuple[bool, np.ndarray, List]:
        """
        Simple frame difference motion detection

        Args:
            frame: Current frame
            prev_frame: Previous frame

        Returns:
            Tuple of (motion_detected, processed_frame, contours)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self.config['detection']['blur_kernel'],
                                       self.config['detection']['blur_kernel']), 0)

        if prev_frame is None:
            return False, frame, []

        # Calculate difference
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, self.config['detection']['sensitivity'],
                              255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=self.config['detection']['dilation_iterations'])

        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        motion = False
        result_frame = frame.copy()

        for contour in contours:
            if cv2.contourArea(contour) < self.config['detection']['min_area']:
                continue

            motion = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return motion, result_frame, contours

    def detect_motion_mog2(self, frame: np.ndarray) -> Tuple[bool, np.ndarray, List]:
        """
        MOG2 background subtraction motion detection

        Args:
            frame: Current frame

        Returns:
            Tuple of (motion_detected, processed_frame, contours)
        """
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(frame)

        # Remove shadows (value 127 in MOG2)
        _, fg_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)

        # Morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        motion = False
        result_frame = frame.copy()

        for contour in contours:
            if cv2.contourArea(contour) < self.config['detection']['min_area']:
                continue

            motion = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw center point
            center_x = x + w // 2
            center_y = y + h // 2
            cv2.circle(result_frame, (center_x, center_y), 4, (0, 0, 255), -1)

        return motion, result_frame, contours

    def process_frame(self, frame: np.ndarray, prev_frame: Optional[np.ndarray] = None) -> Tuple[bool, np.ndarray]:
        """
        Process a single frame for motion detection

        Args:
            frame: Current frame
            prev_frame: Previous frame (for simple algorithm)

        Returns:
            Tuple of (motion_detected, processed_frame)
        """
        algorithm = self.config['detection']['algorithm']

        if algorithm == 'mog2':
            motion, processed_frame, _ = self.detect_motion_mog2(frame)
        else:  # simple
            motion, processed_frame, _ = self.detect_motion_simple(frame, prev_frame)

        # Add timestamp and status overlay
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "MOTION DETECTED" if motion else "Monitoring..."
        color = (0, 0, 255) if motion else (0, 255, 0)

        cv2.putText(processed_frame, timestamp, (10, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(processed_frame, status, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Add FPS counter
        cv2.putText(processed_frame, f"FPS: {self.stats['fps']:.1f}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return motion, processed_frame

    def record_motion_event(self, started: bool):
        """
        Record motion event (start or stop)

        Args:
            started: True if motion started, False if stopped
        """
        now = datetime.now()

        if started:
            self.current_event_start = now
            self.stats['total_detections'] += 1
            self.stats['last_detection'] = now
        else:
            if self.current_event_start:
                duration = (now - self.current_event_start).total_seconds()
                self.motion_events.append({
                    'start': self.current_event_start,
                    'end': now,
                    'duration': duration
                })
                self.stats['total_duration'] += duration
                self.current_event_start = None

    def get_statistics(self) -> Dict:
        """Get current statistics"""
        return self.stats.copy()

    def get_motion_events(self) -> List[Dict]:
        """Get all motion events"""
        return self.motion_events.copy()

    def save_events_to_csv(self, filename: str = "motion_events.csv"):
        """
        Save motion events to CSV file

        Args:
            filename: Output filename
        """
        import pandas as pd

        if not self.motion_events:
            return

        df = pd.DataFrame([
            {
                'Started': event['start'],
                'Stopped': event['end'],
                'Duration (seconds)': event['duration']
            }
            for event in self.motion_events
        ])

        df.to_csv(filename, index=False)

    def cleanup(self):
        """Cleanup resources"""
        self.is_running = False

        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()
