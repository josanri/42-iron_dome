set -e

sh -c "echo > /data/ha Buenos dias que tal todo el mundo esto es un archivo completamente normalnnja knabsio ña  aa aa akjhqube dnddm m nmwqeioq kj mnw mnnu kj kmn"
sh -c "echo > /data/he contenido"
sleep 2
python3 irondome.py --path /data
sleep 1
mv /data/he /data/he.txt
sleep 1
sh -c " echo >> ha '                                                                                                                                                                                                                                                                                                                                                                                                                          '"

tail -n 50 -f /var/log/irondome/irondome.log