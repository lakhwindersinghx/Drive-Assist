# Raspberry Pi 5 – Reproducible OpenCV + GStreamer setup inside **pyenv**

These are the exact steps we followed on a fresh 64‑bit **Raspberry Pi OS Bookworm** (June 2025) to get a working `cv2` build with full **GStreamer** camera support inside a dedicated `pyenv` virtual‑environment.

> **Scope** – This guide stops once the camera pipeline produces frames. PyCoral installation is documented separately.

---

## 1  System prerequisites

| Item    | Version / note                                   |
| ------- | ------------------------------------------------ |
| SoC     | Raspberry Pi 5 (BCM2712)                         |
| OS      | Raspberry Pi OS Bookworm 64‑bit (>= April 2025)  |
| Camera  | Official HQ / IMX708 – works with `libcamerasrc` |
| GPU mem | **≥128 MB** (`raspi-config`)                     |

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 1.1  Build tool‑chain & libraries

```bash
sudo apt install -y --no-install-recommends \
  build-essential git cmake pkg-config ninja-build \
  libgtk-3-dev libcanberra-gtk3-dev \
  libatlas-base-dev libjpeg-dev libtiff-dev libpng-dev \
  libavcodec-dev libavformat-dev libswscale-dev libavutil-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-base libwebp-dev libopenjp2-7-dev \
  libtbb-dev libhdf5-dev python3-dev python3-pip
```

> **Why?**  The two `libgstreamer…-dev` packages expose headers CMake needs to say *GStreamer YES*.

---

## 2  Install **pyenv** + virtual‑env

```bash
# 2.1  Install pyenv & helpers
curl https://pyenv.run | bash

# 2.2  Add to shell  ➜  ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
[[ -d "$PYENV_ROOT/bin" ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

exec $SHELL   # reload

# 2.3  Python 3.9 is the sweet‑spot for PyCoral (as of Jul 2025)
pyenv install 3.9.16
pyenv virtualenv 3.9.16 kyros-coral
pyenv activate kyros-coral   # prompt becomes (kyros-coral)

# Quality‑of‑life
pip install --upgrade pip wheel setuptools
```

---

## 3  Purge any pre‑built OpenCV wheels (very important)

```bash
pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python || true
```

> Leaving wheels installed will shadow the custom build and break GStreamer.

---

## 4  Build OpenCV 4.9.0 with contrib + GStreamer

```bash
mkdir -p ~/src && cd ~/src

# 4.1  Clone matching tags
git clone --depth 1 -b 4.9.0 https://github.com/opencv/opencv.git
git clone --depth 1 -b 4.9.0 https://github.com/opencv/opencv_contrib.git

# 4.2  Configure
cd opencv && mkdir build && cd build

# Helper vars so CMake finds the venv correctly
PYTHON_SITE=$(python - <<'PY'
import sysconfig, pathlib; print(pathlib.Path(sysconfig.get_paths()['purelib']).as_posix())
PY)

cmake .. \
  -D CMAKE_BUILD_TYPE=Release \
  -D WITH_GSTREAMER=ON \
  -D OPENCV_GENERATE_PKGCONFIG=ON \
  -D OPENCV_EXTRA_MODULES_PATH=~/src/opencv_contrib/modules \
  -D PYTHON_EXECUTABLE=$(which python) \
  -D PYTHON3_PACKAGES_PATH="${PYTHON_SITE}" \
  -D BUILD_opencv_python3=ON \
  -D BUILD_EXAMPLES=OFF

# 4.3  Compile only the Python bindings (quickest route)
make -j$(nproc) opencv_python3

# 4.4  Install & refresh linker cache
sudo make install
sudo ldconfig
```

> **Tip** – `make -j$(nproc)` took ≈ 45 min on an actively‑cooled Pi 5.

---

## 5  Smoke‑test inside the env

```bash
python - <<'PY'
import cv2, re
print('cv2  :', cv2.__file__)
print('vers :', cv2.__version__)
print('GST? :', re.search(r"GStreamer:\s*YES", cv2.getBuildInformation()) is not None)
PY
```

Expected:

```
cv2  : …/kyros-coral/lib/python3.9/site-packages/cv2/__init__.py
vers : 4.9.0
GST? : True
```

---

## 6  Camera sanity check

```bash
python - <<'PY'
import cv2
pipe = ("libcamerasrc ! "
        "video/x-raw,format=NV12,width=640,height=480,framerate=30/1 ! "
        "videoconvert ! appsink")
cap = cv2.VideoCapture(pipe, cv2.CAP_GSTREAMER)
print("Opened:", cap.isOpened())
print("1st frame OK:", cap.read()[0] if cap.isOpened() else None)
cap.release()
PY
```

If both booleans are `True`, the stack is sound.

---

## 7  Run the full preview script

```bash
cd ~/kyros-adas-vision-mvp     # wherever camera_test.py lives
python camera_test.py          # press q to quit
```

### Common tweaks

| Symptom                | Fix                                                       |
| ---------------------- | --------------------------------------------------------- |
| *Purple/green preview* | Add `video/x-raw,format=BGR !` after `videoconvert`.      |
| Drops frames instantly | Temporarily remove `drop=1 sync=false` to see real error. |
| Pipeline won’t open    | Try lower res `w=640, h=480`; confirm GPU\_mem ≥128 MB.   |

---

## 8  Ready for PyCoral

With OpenCV settled in the same venv, proceed to the **README\_PyCoral\_RPi5.md** steps starting at *Install PyCoral & Dependencies*.

---

### Change‑log / verified versions

- 2025‑07‑06   Guide written after successful build on Pi OS Bookworm (kernel 6.12.34, GCC 12.2.0).
- OpenCV 4.9.0 + contrib, GStreamer 1.22.0, libcamera 0.5.0.

---

Enjoy reproducible Raspberry‑Pi camera pipelines!

