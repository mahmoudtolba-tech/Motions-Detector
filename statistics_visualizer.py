"""
Statistics and Visualization Module
Provides advanced analytics and visual reports for motion detection data
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import seaborn as sns


class StatisticsVisualizer:
    """
    Creates visualizations and analytics for motion detection data
    """

    def __init__(self, events: List[Dict] = None):
        """
        Initialize visualizer

        Args:
            events: List of motion detection events
        """
        self.events = events or []
        sns.set_style("darkgrid")

    def update_events(self, events: List[Dict]):
        """Update events data"""
        self.events = events

    def get_hourly_distribution(self) -> Dict[int, int]:
        """
        Get distribution of motion events by hour of day

        Returns:
            Dictionary mapping hour (0-23) to count
        """
        hourly_counts = {i: 0 for i in range(24)}

        for event in self.events:
            hour = event['start'].hour
            hourly_counts[hour] += 1

        return hourly_counts

    def get_daily_distribution(self) -> Dict[str, int]:
        """
        Get distribution of motion events by day of week

        Returns:
            Dictionary mapping day name to count
        """
        daily_counts = {
            'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0,
            'Friday': 0, 'Saturday': 0, 'Sunday': 0
        }

        for event in self.events:
            day_name = event['start'].strftime('%A')
            daily_counts[day_name] += 1

        return daily_counts

    def get_duration_statistics(self) -> Dict:
        """
        Calculate duration statistics

        Returns:
            Dictionary with min, max, mean, median durations
        """
        if not self.events:
            return {'min': 0, 'max': 0, 'mean': 0, 'median': 0}

        durations = [event['duration'] for event in self.events]

        return {
            'min': min(durations),
            'max': max(durations),
            'mean': np.mean(durations),
            'median': np.median(durations),
            'std': np.std(durations)
        }

    def get_events_in_timeframe(self, hours: int = 24) -> List[Dict]:
        """
        Get events within specified timeframe

        Args:
            hours: Number of hours to look back

        Returns:
            List of events in timeframe
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        return [e for e in self.events if e['start'] >= cutoff]

    def plot_hourly_distribution(self, fig=None) -> plt.Figure:
        """
        Create bar chart of hourly distribution

        Args:
            fig: Existing figure (optional)

        Returns:
            Matplotlib figure
        """
        if fig is None:
            fig = plt.figure(figsize=(10, 6))

        hourly_data = self.get_hourly_distribution()
        hours = list(hourly_data.keys())
        counts = list(hourly_data.values())

        ax = fig.add_subplot(111)
        ax.bar(hours, counts, color='steelblue', alpha=0.7)
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Number of Detections', fontsize=12)
        ax.set_title('Motion Detection Activity by Hour', fontsize=14, fontweight='bold')
        ax.set_xticks(range(0, 24, 2))
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_daily_distribution(self, fig=None) -> plt.Figure:
        """
        Create bar chart of daily distribution

        Args:
            fig: Existing figure (optional)

        Returns:
            Matplotlib figure
        """
        if fig is None:
            fig = plt.figure(figsize=(10, 6))

        daily_data = self.get_daily_distribution()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        counts = [daily_data[day] for day in days]

        ax = fig.add_subplot(111)
        ax.bar(days, counts, color='coral', alpha=0.7)
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Number of Detections', fontsize=12)
        ax.set_title('Motion Detection Activity by Day', fontsize=14, fontweight='bold')
        ax.set_xticklabels(days, rotation=45)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_duration_histogram(self, fig=None) -> plt.Figure:
        """
        Create histogram of event durations

        Args:
            fig: Existing figure (optional)

        Returns:
            Matplotlib figure
        """
        if fig is None:
            fig = plt.figure(figsize=(10, 6))

        if not self.events:
            return fig

        durations = [event['duration'] for event in self.events]

        ax = fig.add_subplot(111)
        ax.hist(durations, bins=30, color='mediumseagreen', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Duration (seconds)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Motion Event Durations', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        # Add mean line
        mean_duration = np.mean(durations)
        ax.axvline(mean_duration, color='red', linestyle='--', linewidth=2,
                  label=f'Mean: {mean_duration:.1f}s')
        ax.legend()

        plt.tight_layout()
        return fig

    def plot_timeline(self, hours: int = 24, fig=None) -> plt.Figure:
        """
        Create timeline plot of recent events

        Args:
            hours: Number of hours to show
            fig: Existing figure (optional)

        Returns:
            Matplotlib figure
        """
        if fig is None:
            fig = plt.figure(figsize=(12, 6))

        recent_events = self.get_events_in_timeframe(hours)

        if not recent_events:
            return fig

        # Prepare data
        starts = [e['start'] for e in recent_events]
        durations = [e['duration'] for e in recent_events]

        ax = fig.add_subplot(111)

        # Plot events as horizontal bars
        for i, (start, duration) in enumerate(zip(starts, durations)):
            ax.barh(i, duration / 3600, left=mdates.date2num(start),
                   height=0.8, color='orangered', alpha=0.7)

        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Event Number', fontsize=12)
        ax.set_title(f'Motion Events Timeline (Last {hours} hours)',
                    fontsize=14, fontweight='bold')

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.xticks(rotation=45)

        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()

        return fig

    def plot_heatmap(self, fig=None) -> plt.Figure:
        """
        Create heatmap showing activity by hour and day

        Args:
            fig: Existing figure (optional)

        Returns:
            Matplotlib figure
        """
        if fig is None:
            fig = plt.figure(figsize=(12, 6))

        if not self.events:
            return fig

        # Create matrix: days x hours
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        matrix = np.zeros((7, 24))

        for event in self.events:
            day_idx = event['start'].weekday()
            hour_idx = event['start'].hour
            matrix[day_idx, hour_idx] += 1

        ax = fig.add_subplot(111)
        im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')

        # Set ticks
        ax.set_xticks(range(24))
        ax.set_yticks(range(7))
        ax.set_xticklabels(range(24))
        ax.set_yticklabels(days)

        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Day of Week', fontsize=12)
        ax.set_title('Motion Detection Activity Heatmap', fontsize=14, fontweight='bold')

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Number of Detections', rotation=270, labelpad=20)

        plt.tight_layout()
        return fig

    def generate_summary_report(self) -> str:
        """
        Generate text summary report

        Returns:
            Summary report as string
        """
        if not self.events:
            return "No motion events recorded yet."

        total_events = len(self.events)
        duration_stats = self.get_duration_statistics()

        # Time range
        earliest = min(e['start'] for e in self.events)
        latest = max(e['end'] for e in self.events)
        time_span = (latest - earliest).total_seconds() / 3600  # hours

        # Recent activity
        last_24h = len(self.get_events_in_timeframe(24))
        last_hour = len(self.get_events_in_timeframe(1))

        # Peak hours
        hourly_dist = self.get_hourly_distribution()
        peak_hour = max(hourly_dist, key=hourly_dist.get)

        report = f"""
╔══════════════════════════════════════════════════════════╗
║         MOTION DETECTION SUMMARY REPORT                  ║
╚══════════════════════════════════════════════════════════╝

📊 OVERALL STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Events:              {total_events}
  Time Period:               {time_span:.1f} hours
  First Detection:           {earliest.strftime('%Y-%m-%d %H:%M:%S')}
  Latest Detection:          {latest.strftime('%Y-%m-%d %H:%M:%S')}

⏱️  DURATION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Average Duration:          {duration_stats['mean']:.2f} seconds
  Median Duration:           {duration_stats['median']:.2f} seconds
  Shortest Event:            {duration_stats['min']:.2f} seconds
  Longest Event:             {duration_stats['max']:.2f} seconds
  Standard Deviation:        {duration_stats['std']:.2f} seconds

📈 RECENT ACTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Last Hour:                 {last_hour} event(s)
  Last 24 Hours:             {last_24h} event(s)
  Peak Activity Hour:        {peak_hour}:00

🔥 BUSIEST DAY OF WEEK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        daily_dist = self.get_daily_distribution()
        for day, count in sorted(daily_dist.items(), key=lambda x: x[1], reverse=True)[:3]:
            report += f"  {day:12s}             {count} event(s)\n"

        return report

    def export_to_html_report(self, filename: str = "motion_report.html"):
        """
        Export comprehensive HTML report with all visualizations

        Args:
            filename: Output filename
        """
        # Create all plots
        fig1 = self.plot_hourly_distribution()
        fig2 = self.plot_daily_distribution()
        fig3 = self.plot_duration_histogram()
        fig4 = self.plot_heatmap()

        # Save plots as base64
        import io
        import base64

        def fig_to_base64(fig):
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            return base64.b64encode(buf.read()).decode('utf-8')

        img1 = fig_to_base64(fig1)
        img2 = fig_to_base64(fig2)
        img3 = fig_to_base64(fig3)
        img4 = fig_to_base64(fig4)

        plt.close('all')

        # Generate HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Motion Detection Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .section {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart img {{
            max-width: 100%;
            height: auto;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎥 Motion Detection Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="section">
        <h2>Summary</h2>
        <pre>{self.generate_summary_report()}</pre>
    </div>

    <div class="section">
        <h2>Hourly Distribution</h2>
        <div class="chart">
            <img src="data:image/png;base64,{img1}" alt="Hourly Distribution">
        </div>
    </div>

    <div class="section">
        <h2>Daily Distribution</h2>
        <div class="chart">
            <img src="data:image/png;base64,{img2}" alt="Daily Distribution">
        </div>
    </div>

    <div class="section">
        <h2>Duration Analysis</h2>
        <div class="chart">
            <img src="data:image/png;base64,{img3}" alt="Duration Histogram">
        </div>
    </div>

    <div class="section">
        <h2>Activity Heatmap</h2>
        <div class="chart">
            <img src="data:image/png;base64,{img4}" alt="Activity Heatmap">
        </div>
    </div>
</body>
</html>
        """

        with open(filename, 'w') as f:
            f.write(html)

        print(f"Report exported to {filename}")
