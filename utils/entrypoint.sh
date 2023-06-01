set -e

python3 irondome.py --path /data
sleep 1
sh -c "echo > /data/ho la"
sh -c "echo > /data/ho LB"
sleep 1

tail -f /var/log/irondome/irondome.log