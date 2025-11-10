# Quick Start Guide

## Installation (2 minutes)

### Linux / macOS
```bash
chmod +x setup.sh run.sh
./setup.sh
```

### Windows
```cmd
setup.bat
```

## Run the Application

### Linux / macOS
```bash
./run.sh
```

### Windows
```cmd
run.bat
```

## First Time Usage

1. **Click "▶ Start Detection"**
   - The camera will activate
   - Motion detection begins immediately

2. **Adjust Settings (Optional)**
   - Go to "Settings" tab
   - Move "Sensitivity" slider (default: 50)
   - Enable/disable auto-recording

3. **View Statistics**
   - Check "Statistics" tab for real-time data
   - See "Events" tab for motion history

4. **Stop and Export**
   - Click "⏹ Stop Detection"
   - Export data via "Export Events to CSV" button

## Common Settings

| Setting | Low | Medium | High |
|---------|-----|--------|------|
| Sensitivity | 20 | 50 | 80 |
| Min Area | 10000 | 5000 | 2000 |

**Low**: Only large obvious movements
**Medium**: Balanced, recommended
**High**: Very sensitive, catches everything

## Troubleshooting

- **Camera not working?** → Try changing camera index in config.json (0 → 1)
- **Too many false alarms?** → Increase Min Area, lower Sensitivity
- **Missing detections?** → Decrease Min Area, increase Sensitivity

## Files Generated

- `recordings/` - Motion-triggered video recordings
- `snapshots/` - Manual snapshots
- `motion_events.csv` - Event log (after export)
- `config.json` - Your settings

## Need Help?

See the full **README.md** for detailed documentation.

**Enjoy your advanced motion detector!** 🎥
