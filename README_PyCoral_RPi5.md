# README\_PyCoral\_RPi5.md

**Purpose:** This guide provides a reproducible, step-by-step process to set up and verify a Python environment on Raspberry Pi 5 for running Coral Edge TPU demos with the PyCoral API.

---

## 1. System Prerequisites

1. **Add the Coral APT repository & GPG key**

   ```bash
   echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" \
     | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
   curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   ```

   - **Verify:** `OK` from apt-key addition.

2. **Update package list**

   ```bash
   sudo apt-get update
   ```

3. **Install the Edge TPU runtime**

   ```bash
   sudo apt-get install libedgetpu1-std
   ```

   - **Verify:** You should see a message like `libedgetpu1-std is already the newest version (...).`

4. **Re-plug the USB Accelerator**\
   Unplug and replug your Coral USB Accelerator to apply udev rules.

---

## 2. Install Build Dependencies

1. **Clean any partial lists & cache**

   ```bash
   sudo rm -rf /var/lib/apt/lists/*
   sudo apt-get clean
   sudo apt-get update
   ```

2. **Install compilation tools & headers**

   ```bash
   sudo apt-get install -y --fix-missing \
     make build-essential libssl-dev zlib1g-dev libbz2-dev \
     libreadline-dev libsqlite3-dev wget llvm libncurses-dev \
     libncursesw5-dev xz-utils tk-dev libxml2-dev \
     libxmlsec1-dev libffi-dev liblzma-dev curl
   ```

   - **Verify:** No errors during install.

---

## 3. Install & Configure pyenv

1. **Install pyenv**

   ```bash
   curl https://pyenv.run | bash
   ```

2. **Configure your shell**\
   Append the following to `~/.bashrc`:

   ```bash
   export PYENV_ROOT="$HOME/.pyenv"
   [[ -d "$PYENV_ROOT/bin" ]] && export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   ```

3. **Reload your shell**

   ```bash
   exec $SHELL
   ```

4. **Verify pyenv**

   ```bash
   command -v pyenv  # should output 'pyenv'
   ```

---

## 4. Install Python 3.9 via pyenv

1. **Install version 3.9.16**

   ```bash
   pyenv install 3.9.16
   ```

2. **Verify installation**

   ```bash
   pyenv versions  # lists 3.9.16
   ```

---

## 5. Create & Activate Virtual Environment

1. **Remove existing venv (if any)**

   ```bash
   rm -rf kyros-coral
   ```

2. **Create venv named **``

   ```bash
   pyenv virtualenv 3.9.16 kyros-coral
   ```

3. **Activate the environment**

   ```bash
   pyenv activate kyros-coral
   ```

4. **Confirm Python version**

   ```bash
   python --version  # should be Python 3.9.16
   ```

---

## 6. Install PyCoral & Dependencies

1. **Upgrade pip**

   ```bash
   pip install --upgrade pip
   ```

2. **Pin NumPy to <2**\
   PyCoral’s extensions require the NumPy 1.x C‑API:

   ```bash
   pip install "numpy<2"
   ```

   - **Verify:**
     ```bash
     python -c "import numpy; print(numpy.__version__)"
     # Expect 1.x.x
     ```

3. **Install tflite-runtime**

   ```bash
   pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite-runtime
   ```

4. **Install PyCoral**

   ```bash
   pip install --extra-index-url https://google-coral.github.io/py-repo/ "pycoral~=2.0"
   ```

5. **Verify installation**

   ```bash
   python - << 'EOF'
   import numpy, tflite_runtime as trt, pycoral
   print("numpy:", numpy.__version__)
   print("tflite-runtime:", trt.__version__)
   print("pycoral:", pycoral.__version__)
   EOF
   ```

   - **Expect:** numpy 1.x.x, tflite-runtime 2.5.0.post1, pycoral 2.0.0

---

## 7. Run the TFLite Example & Inference

1. **Clone the examples repo**

   ```bash
   cd ~/kyros-adas-vision-mvp  # repo root
   mkdir -p coral && cd coral
   git clone https://github.com/google-coral/pycoral.git
   cd pycoral
   ```

2. **Download model, labels & test image**

   ```bash
   bash examples/install_requirements.sh classify_image.py
   ```

   - **Artifacts fetched:**
     - `mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite`
     - `inat_bird_labels.txt`
     - `parrot.jpg`

3. **Run the classification demo**

   ```bash
   python3 examples/classify_image.py \
     --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
     --labels test_data/inat_bird_labels.txt \
     --input test_data/parrot.jpg
   ```

4. **Expected output**

   ```
   ----INFERENCE TIME----
   Note: The first inference is slow due to model load.
   X.Yms
   X.Yms
   ...
   -------RESULTS--------
   Ara macao (Scarlet Macaw): 0.75781
   ```

5. **Verify inference**

   - Ensure you see timing metrics (\~15ms first, \~4ms subsequent) and a correct bird label.

---

*End of README: reproducible PyCoral setup & inference on Raspberry Pi 5.*

