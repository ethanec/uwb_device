# uwb_device
A repository with codes used on Mini4, a UWB device. It can be use as device calibration, get distance between anchors and tags, also localization in our diractory.

## Requirements
```bash 
python == 2.7.17
pandas == 0.24.2
numpy == 1.13.3
matplotlib == 2.1.1
csv == 1.0
serial == 3.4
eigen == 3.3.7
```

## Calibration
For the UWB device, the distance got from Mini4 naturally has a bias from real distance depending on the range of two antenna, the temperature and other factors.
To alleviate the difference, we measure the raw data at many different ranges from 2 meters to 30 meters.

### recording raw data
```bash
$ python scripts/uwb_csv_record.py 
```

### Filter the missing data
```bash
$ python scripts/preprocess.py
```

### calculating the standard deviation and the mean error
```bash
$ python scripts/cal_std_mean.py
```
update the results in `uwb_start.py`

## Measure distance
The bias is approximated by linearization of measured ranges.
```bash
$ python scripts/uwb_start.py
```

## Navigation
The algorithm is designed using "Least square".
### Set up Anchors (at least 3 anchors)
Measure the positions of your anchors and update A1, A2, A3 in the `uwb_positioning.cpp`
```cpp
    A1 << 0, 0, 1;
    A2 << 1, 0, 0;
    A3 << 0, 1, 0;
    VectorXd A[3] = {A1, A2, A3};
```
After recompiling,
```bash
$ rosrun uwb uwb_positioning
```



