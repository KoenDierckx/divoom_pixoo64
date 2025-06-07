# Divoom Pixoo64 Integration for Home Assistant

This integration allows you to control your Divoom Pixoo64 device from Home Assistant.

## Features

- Automatic discovery of Pixoo64 devices on your network
- Manual configuration option with IP address
- Control brightness
- Display text on the screen with customizable color
- Display images from local files
- Monitor device connectivity
- Efficient state updates using DataUpdateCoordinator

## Installation

### Using HACS (recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Go to HACS > Integrations
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add the URL `https://github.com/KoenDierckx/home-assistant-divoom-pixoo64` with category "Integration"
5. Click "Add"
6. Search for "Divoom Pixoo64" and install it
7. Restart Home Assistant

### Manual Installation

1. Download the latest release from GitHub
2. Extract the `custom_components/divoom_pixoo64` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

The integration can be set up through the Home Assistant UI:

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Divoom Pixoo64"
4. Enter the IP address of your Pixoo64 device
5. Follow the on-screen instructions

## Services

This integration provides the following services:

### `divoom_pixoo64.display_text`

Display text on the Pixoo64 device.

| Parameter | Description                                        | Required | Default  |
|-----------|---------------------------------------------------|----------|----------|
| text      | Text to display on the device                     | Yes      | -        |
| color     | Color of the text in hex format (e.g., FFFFFF)    | No       | FFFFFF   |

### `divoom_pixoo64.display_image`

Display an image on the Pixoo64 device.

| Parameter  | Description                 | Required | Default |
|------------|-----------------------------|----------|---------|
| image_path | Path to the image to display| Yes      | -       |

### `divoom_pixoo64.set_brightness`

Set the brightness of the Pixoo64 device.

| Parameter  | Description                 | Required | Default |
|------------|-----------------------------|----------|---------|
| brightness | Brightness level (0-100)    | Yes      | -       |

## Entities

### Binary Sensor

- **Connectivity**: Shows whether the device is reachable or not

### Media Player

- **Display**: Controls the display with on/off and brightness adjustment

## Technical Implementation

This integration uses Home Assistant's DataUpdateCoordinator to efficiently manage API requests and state updates. This ensures:

- Reduced API calls to prevent rate limiting and improve performance
- Consistent state updates across multiple entities
- Better error handling and recovery
- Automatic data refresh at configurable intervals

## Troubleshooting

- Make sure your Pixoo64 device is connected to the same network as your Home Assistant instance
- Check that you have entered the correct IP address
- Verify that your device is powered on and operational
- Check the Home Assistant logs for error messages

## Credits

This integration uses the [aiopixooapi](https://pypi.org/project/aiopixooapi/) library.
