echo 'Alpha variation'
echo 'Auckland'
python ping.py www.auckland.ac.nz 0.05 10 1
python ping.py www.auckland.ac.nz 0.10 10 1
python ping.py www.auckland.ac.nz 0.15 10 1
python ping.py www.auckland.ac.nz 0.20 10 1
echo 'Cambridge'
python ping.py www.cam.ac.uk 0.05 10 1
python ping.py www.cam.ac.uk 0.10 10 1
python ping.py www.cam.ac.uk 0.15 10 1
python ping.py www.cam.ac.uk 0.20 10 1
echo 'Beijing'
python ping.py www.pku.edu.cn 0.05 10 1
python ping.py www.pku.edu.cn 0.10 10 1
python ping.py www.pku.edu.cn 0.15 10 1
python ping.py www.pku.edu.cn 0.20 10 1
echo 'Rhodes'
python ping.py www.ru.ac.za 0.05 10 1
python ping.py www.ru.ac.za 0.10 10 1
python ping.py www.ru.ac.za 0.15 10 1
python ping.py www.ru.ac.za 0.20 10 1
echo '------------------'
echo 'Timeout variation'
echo 'Auckland'
python ping.py www.auckland.ac.nz 0.15 10 0.1
python ping.py www.auckland.ac.nz 0.15 10 0.25
python ping.py www.auckland.ac.nz 0.15 10 0.5
python ping.py www.auckland.ac.nz 0.15 10 1
python ping.py www.auckland.ac.nz 0.15 10 2
echo 'Cambridge'
python ping.py www.cam.ac.uk 0.15 10 0.1
python ping.py www.cam.ac.uk 0.15 10 0.25
python ping.py www.cam.ac.uk 0.15 10 0.5
python ping.py www.cam.ac.uk 0.15 10 1
python ping.py www.cam.ac.uk 0.15 10 2
echo 'Beijing'
python ping.py www.pku.edu.cn 0.15 10 0.1
python ping.py www.pku.edu.cn 0.15 10 0.25
python ping.py www.pku.edu.cn 0.15 10 0.5
python ping.py www.pku.edu.cn 0.15 10 1
python ping.py www.pku.edu.cn 0.15 10 2
echo 'Rhodes'
python ping.py www.ru.ac.za 0.15 10 0.1
python ping.py www.ru.ac.za 0.15 10 0.25
python ping.py www.ru.ac.za 0.15 10 0.5
python ping.py www.ru.ac.za 0.15 10 1
python ping.py www.ru.ac.za 0.15 10 2
echo '------------------'
echo 'Count variation'
echo 'Auckland'
python ping.py www.auckland.ac.nz 0.15 10 1
python ping.py www.auckland.ac.nz 0.15 20 1
python ping.py www.auckland.ac.nz 0.15 50 1
python ping.py www.auckland.ac.nz 0.15 100 1
echo 'Cambridge'
python ping.py www.cam.ac.uk 0.15 10 1
python ping.py www.cam.ac.uk 0.15 20 1
python ping.py www.cam.ac.uk 0.15 50 1
python ping.py www.cam.ac.uk 0.15 100 1
echo 'Beijing'
python ping.py www.pku.edu.cn 0.15 10 1
python ping.py www.pku.edu.cn 0.15 20 1
python ping.py www.pku.edu.cn 0.15 50 1
python ping.py www.pku.edu.cn 0.15 100 1
echo 'Rhodes'
python ping.py www.ru.ac.za 0.15 10 1
python ping.py www.ru.ac.za 0.15 20 1
python ping.py www.ru.ac.za 0.15 50 1
python ping.py www.ru.ac.za 0.15 100 1


