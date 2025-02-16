# The Dual Syringe Continuous Pumping Mechanism (DSCPM)

## Repository for the Article: *A Continuous, Low Flow, and Multiplexing Pumping System for Microfluidics Applications*

This repository contains all software, hardware schematics, and supplementary materials associated with the publication:

[Preprint on bioRxiv](https://www.biorxiv.org/content/10.1101/2024.08.16.608339v1)

### **Contents of This Repository**
- **Arduino Code:**
  - DSCPM 2-3/1-2
  - DSCPM 2-2
  - Fluidic Multiplexers
- **Python Scripts:**
  - Edge-detection scripts for generating volume-infused vs. time and flow rate vs. time plots from pre-cropped horizontal (left-to-right) videos of dyed fluid infusing into micro-bore tubing.  
  - *Note:* Generative AI was utilized in the development of these scripts. The authors have rigorously validated the generated quantitative data against raw video data and assume full responsibility for its accuracy.
- **3D Printable Components:**
  - STL files for DSCPM parts.

---

## **Repository Structure**

### **Main Directory**
- **Appendix A**  
  - Hardware and microfluidic chamber design files.
  - `.stl` files for 3D-printed components (e.g., syringe plunger, valve holder).
  - `.gds` files for microfluidic monolayer geometries (Layer 1 & Layer 2).

- **Appendix B**  
  - Integrated Arduino `.ino` files for DSCPM pumps and fluidic multiplexers.
  - Graphical User Interface (GUI) that interfaces with the Arduino via serial communication to control the pump system.

- **Appendix C**  
  - Data files and analysis scripts.
  - Jupyter notebooks (`.ipynb`) and MATLAB scripts (`.m`) are used to process experimental data presented in the paper.

