"""
Advanced Motion Detector GUI
Modern user interface using customtkinter
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import json
from pathlib import Path
import numpy as np
from motion_detector_core import MotionDetectorCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class MotionDetectorGUI:
    """
    Modern GUI for Advanced Motion Detector
    """

    def __init__(self):
        """Initialize the GUI"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Advanced Motion Detector Pro")
        self.root.geometry("1400x900")

        # Motion detector core
        self.detector = None
        self.config = self._load_config()

        # Video recording
        self.video_writer = None
        self.is_recording = False

        # Threading
        self.capture_thread = None
        self.is_running = False
        self.prev_frame_gray = None

        # UI Components
        self.video_label = None
        self.status_label = None
        self.detection_count_label = None
        self.recording_status_label = None

        # Initialize UI
        self._create_ui()

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _load_config(self) -> dict:
        """Load configuration from file or create default"""
        config_file = Path("config.json")

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")

        # Default configuration
        config = {
            'camera': {
                'index': 0,
                'width': 640,
                'height': 480,
                'fps': 30
            },
            'detection': {
                'algorithm': 'mog2',
                'sensitivity': 50,
                'min_area': 5000,
                'bg_threshold': 16,
                'blur_kernel': 21,
                'dilation_iterations': 2
            },
            'recording': {
                'enabled': True,
                'codec': 'mp4v',
                'output_dir': 'recordings'
            },
            'notifications': {
                'enabled': False,
                'email': '',
                'cooldown': 60
            }
        }

        self._save_config(config)
        return config

    def _save_config(self, config: dict = None):
        """Save configuration to file"""
        if config is None:
            config = self.config

        try:
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def _create_ui(self):
        """Create the user interface"""
        # Create main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Video feed and controls
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Title
        title = ctk.CTkLabel(left_panel, text="🎥 Advanced Motion Detector Pro",
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10)

        # Video display
        video_frame = ctk.CTkFrame(left_panel, fg_color="black")
        video_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.video_label = ctk.CTkLabel(video_frame, text="No Camera Feed",
                                       font=ctk.CTkFont(size=20))
        self.video_label.pack(expand=True)

        # Status bar
        status_frame = ctk.CTkFrame(left_panel)
        status_frame.pack(fill="x", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(status_frame, text="Status: Idle",
                                        font=ctk.CTkFont(size=14))
        self.status_label.pack(side="left", padx=10)

        self.detection_count_label = ctk.CTkLabel(status_frame, text="Detections: 0",
                                                  font=ctk.CTkFont(size=14))
        self.detection_count_label.pack(side="left", padx=10)

        self.recording_status_label = ctk.CTkLabel(status_frame, text="⚫ Not Recording",
                                                   font=ctk.CTkFont(size=14))
        self.recording_status_label.pack(side="right", padx=10)

        # Control buttons
        control_frame = ctk.CTkFrame(left_panel)
        control_frame.pack(fill="x", padx=10, pady=10)

        self.start_btn = ctk.CTkButton(control_frame, text="▶ Start Detection",
                                       command=self._start_detection,
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       height=40, fg_color="green", hover_color="darkgreen")
        self.start_btn.pack(side="left", padx=5, expand=True, fill="x")

        self.stop_btn = ctk.CTkButton(control_frame, text="⏹ Stop Detection",
                                     command=self._stop_detection,
                                     font=ctk.CTkFont(size=16, weight="bold"),
                                     height=40, fg_color="red", hover_color="darkred",
                                     state="disabled")
        self.stop_btn.pack(side="left", padx=5, expand=True, fill="x")

        self.snapshot_btn = ctk.CTkButton(control_frame, text="📷 Snapshot",
                                         command=self._take_snapshot,
                                         font=ctk.CTkFont(size=16),
                                         height=40, state="disabled")
        self.snapshot_btn.pack(side="left", padx=5, expand=True, fill="x")

        # Right panel - Settings and Statistics
        right_panel = ctk.CTkFrame(main_container, width=400)
        right_panel.pack(side="right", fill="both", padx=(5, 0))
        right_panel.pack_propagate(False)

        # Tabview for settings and stats
        self.tabview = ctk.CTkTabview(right_panel)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.tabview.add("Settings")
        self.tabview.add("Statistics")
        self.tabview.add("Events")

        self._create_settings_tab()
        self._create_statistics_tab()
        self._create_events_tab()

    def _create_settings_tab(self):
        """Create settings tab"""
        settings_tab = self.tabview.tab("Settings")

        # Detection Settings
        detection_frame = ctk.CTkFrame(settings_tab)
        detection_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(detection_frame, text="Detection Settings",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Algorithm selection
        ctk.CTkLabel(detection_frame, text="Algorithm:").pack(anchor="w", padx=10)
        self.algorithm_var = ctk.StringVar(value=self.config['detection']['algorithm'])
        algorithm_menu = ctk.CTkOptionMenu(detection_frame, values=["simple", "mog2"],
                                          variable=self.algorithm_var,
                                          command=self._update_algorithm)
        algorithm_menu.pack(fill="x", padx=10, pady=5)

        # Sensitivity slider
        ctk.CTkLabel(detection_frame, text="Sensitivity:").pack(anchor="w", padx=10)
        self.sensitivity_var = ctk.IntVar(value=self.config['detection']['sensitivity'])
        sensitivity_slider = ctk.CTkSlider(detection_frame, from_=10, to=100,
                                          variable=self.sensitivity_var,
                                          command=self._update_sensitivity)
        sensitivity_slider.pack(fill="x", padx=10, pady=5)
        self.sensitivity_label = ctk.CTkLabel(detection_frame,
                                             text=f"Value: {self.sensitivity_var.get()}")
        self.sensitivity_label.pack()

        # Minimum area slider
        ctk.CTkLabel(detection_frame, text="Minimum Motion Area:").pack(anchor="w", padx=10)
        self.min_area_var = ctk.IntVar(value=self.config['detection']['min_area'])
        area_slider = ctk.CTkSlider(detection_frame, from_=1000, to=20000,
                                   variable=self.min_area_var,
                                   command=self._update_min_area)
        area_slider.pack(fill="x", padx=10, pady=5)
        self.min_area_label = ctk.CTkLabel(detection_frame,
                                          text=f"Value: {self.min_area_var.get()}")
        self.min_area_label.pack()

        # Recording Settings
        recording_frame = ctk.CTkFrame(settings_tab)
        recording_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(recording_frame, text="Recording Settings",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        self.recording_enabled_var = ctk.BooleanVar(value=self.config['recording']['enabled'])
        recording_checkbox = ctk.CTkCheckBox(recording_frame, text="Auto-record on motion",
                                            variable=self.recording_enabled_var,
                                            command=self._update_recording)
        recording_checkbox.pack(padx=10, pady=5)

        # Export buttons
        export_frame = ctk.CTkFrame(settings_tab)
        export_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(export_frame, text="Data Export",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        ctk.CTkButton(export_frame, text="Export Events to CSV",
                     command=self._export_to_csv).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(export_frame, text="Save Configuration",
                     command=lambda: self._save_config()).pack(fill="x", padx=10, pady=5)

    def _create_statistics_tab(self):
        """Create statistics tab"""
        stats_tab = self.tabview.tab("Statistics")

        # Statistics display
        self.stats_frame = ctk.CTkFrame(stats_tab)
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.stats_frame, text="Detection Statistics",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        self.total_detections_label = ctk.CTkLabel(self.stats_frame,
                                                   text="Total Detections: 0",
                                                   font=ctk.CTkFont(size=14))
        self.total_detections_label.pack(pady=5)

        self.total_duration_label = ctk.CTkLabel(self.stats_frame,
                                                text="Total Duration: 0s",
                                                font=ctk.CTkFont(size=14))
        self.total_duration_label.pack(pady=5)

        self.last_detection_label = ctk.CTkLabel(self.stats_frame,
                                                text="Last Detection: Never",
                                                font=ctk.CTkFont(size=14))
        self.last_detection_label.pack(pady=5)

        self.avg_duration_label = ctk.CTkLabel(self.stats_frame,
                                              text="Avg Duration: 0s",
                                              font=ctk.CTkFont(size=14))
        self.avg_duration_label.pack(pady=5)

        # Refresh button
        ctk.CTkButton(self.stats_frame, text="Refresh Statistics",
                     command=self._update_statistics_display).pack(pady=10)

    def _create_events_tab(self):
        """Create events tab"""
        events_tab = self.tabview.tab("Events")

        # Events list
        ctk.CTkLabel(events_tab, text="Recent Motion Events",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Scrollable frame for events
        self.events_scroll = ctk.CTkScrollableFrame(events_tab)
        self.events_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Clear events button
        ctk.CTkButton(events_tab, text="Clear Event History",
                     command=self._clear_events).pack(pady=5)

    def _start_detection(self):
        """Start motion detection"""
        # Initialize detector
        self.detector = MotionDetectorCore(self.config)

        if not self.detector.initialize_camera():
            messagebox.showerror("Error", "Failed to initialize camera!")
            return

        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.snapshot_btn.configure(state="normal")
        self.status_label.configure(text="Status: Running")

        # Start capture thread
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

        # Start stats update
        self._update_statistics_display()

    def _stop_detection(self):
        """Stop motion detection"""
        self.is_running = False

        if self.capture_thread:
            self.capture_thread.join(timeout=2)

        if self.detector:
            self.detector.cleanup()

        if self.video_writer:
            self.video_writer.release()
            self.is_recording = False

        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.snapshot_btn.configure(state="disabled")
        self.status_label.configure(text="Status: Stopped")
        self.recording_status_label.configure(text="⚫ Not Recording")

        # Update statistics one final time
        self._update_statistics_display()
        self._update_events_display()

    def _capture_loop(self):
        """Main capture and processing loop"""
        fps_counter = 0
        fps_start_time = time.time()
        motion_state = False

        while self.is_running:
            if not self.detector.cap or not self.detector.cap.isOpened():
                break

            ret, frame = self.detector.cap.read()
            if not ret:
                continue

            # Process frame for motion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            motion, processed_frame = self.detector.process_frame(frame, self.prev_frame_gray)
            self.prev_frame_gray = gray

            # Handle motion events
            if motion and not motion_state:
                motion_state = True
                self.detector.record_motion_event(started=True)

                # Start recording if enabled
                if self.config['recording']['enabled'] and not self.is_recording:
                    self._start_recording(frame)

            elif not motion and motion_state:
                motion_state = False
                self.detector.record_motion_event(started=False)

                # Stop recording
                if self.is_recording:
                    self._stop_recording()

            # Write frame to video if recording
            if self.is_recording and self.video_writer:
                self.video_writer.write(processed_frame)

            # Update FPS
            fps_counter += 1
            if time.time() - fps_start_time >= 1.0:
                self.detector.stats['fps'] = fps_counter / (time.time() - fps_start_time)
                fps_counter = 0
                fps_start_time = time.time()

            # Display frame in GUI
            self._update_video_display(processed_frame)

            # Small delay
            time.sleep(0.01)

    def _update_video_display(self, frame):
        """Update video display in GUI"""
        try:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize for display
            height, width = frame_rgb.shape[:2]
            max_width = 800
            if width > max_width:
                scale = max_width / width
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame_rgb = cv2.resize(frame_rgb, (new_width, new_height))

            # Convert to PhotoImage
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update label
            self.video_label.configure(image=imgtk, text="")
            self.video_label.image = imgtk

        except Exception as e:
            print(f"Error updating display: {e}")

    def _start_recording(self, frame):
        """Start video recording"""
        try:
            # Create recordings directory
            Path(self.config['recording']['output_dir']).mkdir(exist_ok=True)

            # Generate filename
            filename = f"{self.config['recording']['output_dir']}/motion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*self.config['recording']['codec'])
            fps = self.config['camera']['fps']
            frame_size = (frame.shape[1], frame.shape[0])

            self.video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
            self.is_recording = True
            self.recording_status_label.configure(text="🔴 Recording")

        except Exception as e:
            print(f"Error starting recording: {e}")

    def _stop_recording(self):
        """Stop video recording"""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

        self.is_recording = False
        self.recording_status_label.configure(text="⚫ Not Recording")

    def _take_snapshot(self):
        """Take a snapshot of current frame"""
        if self.detector and self.detector.cap:
            ret, frame = self.detector.cap.read()
            if ret:
                # Create snapshots directory
                Path("snapshots").mkdir(exist_ok=True)

                filename = f"snapshots/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)
                messagebox.showinfo("Snapshot", f"Snapshot saved to {filename}")

    def _update_algorithm(self, choice):
        """Update detection algorithm"""
        self.config['detection']['algorithm'] = choice
        if self.detector:
            self.detector.config['detection']['algorithm'] = choice

    def _update_sensitivity(self, value):
        """Update sensitivity setting"""
        val = int(float(value))
        self.config['detection']['sensitivity'] = val
        self.sensitivity_label.configure(text=f"Value: {val}")
        if self.detector:
            self.detector.config['detection']['sensitivity'] = val

    def _update_min_area(self, value):
        """Update minimum area setting"""
        val = int(float(value))
        self.config['detection']['min_area'] = val
        self.min_area_label.configure(text=f"Value: {val}")
        if self.detector:
            self.detector.config['detection']['min_area'] = val

    def _update_recording(self):
        """Update recording setting"""
        self.config['recording']['enabled'] = self.recording_enabled_var.get()
        if self.detector:
            self.detector.config['recording']['enabled'] = self.recording_enabled_var.get()

    def _update_statistics_display(self):
        """Update statistics display"""
        if not self.detector:
            return

        stats = self.detector.get_statistics()
        events = self.detector.get_motion_events()

        self.total_detections_label.configure(text=f"Total Detections: {stats['total_detections']}")
        self.total_duration_label.configure(text=f"Total Duration: {stats['total_duration']:.1f}s")

        if stats['last_detection']:
            last = stats['last_detection'].strftime('%Y-%m-%d %H:%M:%S')
            self.last_detection_label.configure(text=f"Last Detection: {last}")

        if events:
            avg_duration = sum(e['duration'] for e in events) / len(events)
            self.avg_duration_label.configure(text=f"Avg Duration: {avg_duration:.1f}s")

        self.detection_count_label.configure(text=f"Detections: {stats['total_detections']}")

        # Schedule next update
        if self.is_running:
            self.root.after(1000, self._update_statistics_display)

    def _update_events_display(self):
        """Update events display"""
        if not self.detector:
            return

        # Clear existing events
        for widget in self.events_scroll.winfo_children():
            widget.destroy()

        events = self.detector.get_motion_events()

        if not events:
            ctk.CTkLabel(self.events_scroll, text="No events recorded yet").pack(pady=10)
            return

        # Display last 20 events
        for event in reversed(events[-20:]):
            event_frame = ctk.CTkFrame(self.events_scroll)
            event_frame.pack(fill="x", padx=5, pady=2)

            start_time = event['start'].strftime('%H:%M:%S')
            duration = event['duration']

            ctk.CTkLabel(event_frame, text=f"🔴 {start_time} - Duration: {duration:.1f}s",
                        font=ctk.CTkFont(size=12)).pack(anchor="w", padx=5, pady=2)

    def _clear_events(self):
        """Clear event history"""
        if messagebox.askyesno("Confirm", "Clear all event history?"):
            if self.detector:
                self.detector.motion_events.clear()
                self._update_events_display()

    def _export_to_csv(self):
        """Export events to CSV"""
        if not self.detector:
            messagebox.showwarning("Warning", "No detection data available")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            self.detector.save_events_to_csv(filename)
            messagebox.showinfo("Success", f"Events exported to {filename}")

    def _on_closing(self):
        """Handle window close event"""
        if self.is_running:
            self._stop_detection()

        self._save_config()
        self.root.destroy()

    def run(self):
        """Run the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MotionDetectorGUI()
    app.run()
