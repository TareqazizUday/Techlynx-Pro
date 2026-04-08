#!/bin/bash
# Run THIS on the EC2 server (Linux), NOT on Windows.
# After you upload code from your PC, SSH in and:
#   cd ~/techlynxpro && chmod +x server_update.sh update_code.sh && ./server_update.sh
#
# Same as: ./update_code.sh (migrate, collectstatic, restart gunicorn/nginx)

set -e
cd "$(dirname "$0")"
exec ./update_code.sh
