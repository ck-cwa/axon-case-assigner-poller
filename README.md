# Axon Internal Case Number Assigner

A Python polling service for Axon's Evidence.com API that auto-assigns sequential internal case numbers.

## Features

- Polls for new cases every 60 seconds
- Assigns internal numbers in the format `YY–NNNNN`
- Ignores cases already numbered or from previous years

## Deployment (Railway)

1. Add environment variables:
   - `AXON_API_KEY`
   - `AXON_AGENCY_ID`

2. Deploy via Railway dashboard or CLI.

## License

MIT