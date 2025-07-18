# Drive-Assist: Real-Time Object Detection with Raspberry Pi & Coral USB Accelerator 

This project demonstrates a lightweight **Advanced Driver Assistance System (ADAS)** built using a **Raspberry Pi 5** and **Google Coral USB Edge TPU**. It showcases how cost-effective edge devices can be used for **real-time object detection** with high performance and low power consumption.

https://github.com/user-attachments/assets/f5ef9654-1c15-45a5-8d49-28ad03873c8a

## 🛠 Hardware & Software Stack

- **Compute**: Raspberry Pi 5  
- **Accelerator**: Coral USB Edge TPU  
- **Camera**: Raspberry Pi Camera v2  
- **OS**: Raspberry Pi OS (Bullseye)  
- **ML Framework**: TensorFlow Lite  
- **Libraries**: PyCoral, GStreamer  
- **Language**: Python 3.9  

## ⚙️ Implementation Highlights

- Runs **MobileNet SSD v2 (INT8 quantized)** models optimized for Edge TPU.
- Utilizes **asynchronous processing** and **GStreamer pipelines** for real-time performance.
- **Inference Speed**: ~20–25 FPS  
- **Latency**: <50ms per frame  
- **Power Draw**: Under 5W  

## 🧠 Key Challenges & Solutions

- **Model Compatibility**: Used Coral-optimized INT8 models to avoid inference errors.
- **Dependency Conflicts**: Resolved using isolated Python environments (`pyenv`).
- **Camera Bottlenecks**: Boosted performance with GStreamer and NumPy-based frame handling.

## 📊 Outcome & Suitability

- Reliable real-time object detection on constrained hardware.
- Ideal for:
  - Rapid prototyping of edge AI systems  
  - Budget-friendly embedded ADAS solutions  
  - Low-power, portable IoT devices

## 📚 What I Learned

- Importance of using **TPU-compatible models** and proper **quantization**
- Hardware acceleration significantly boosts edge AI feasibility
- Optimization techniques like **asynchronous processing** are game changers

## ✅ Conclusion

This project proves that real-time ADAS applications can be built **without expensive GPUs**. With proper optimization, the **Raspberry Pi + Coral TPU combo** delivers an excellent balance of speed, accuracy, and efficiency — ideal for makers, researchers, and early-stage product developers.

---

