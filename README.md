# AXI Data Analysis
AXI (Advanced eXtensible Interface) is a flexible and comprehensive interface protocol used to enable high-speed communication between components in an integrated circuit. It is widely used in systems that require efficient data transfer and processing.

## Excel Sheet Requirements
To use this application, your Excel sheet should be structured with the following headers:

- Txn_type: Read/ Write instructions
- Txn_id: (Integer)
- Address: (String)
- Address_type: Fixed/ INCR instructions
- Number of data bytes: 2^n (Integer)
- Start time (ns): (Float/ Decimal)
- End time (ns): (Float/ Decimal)

These headers are essential for the correct functioning of the data analysis features in the application. Make sure your Excel sheet adheres to this format.

## Front-End Overview:
The front-end of the application is designed to be user-friendly and intuitive. Below are some images showcasing different parts of the user interface, including various graphs and charts that the application can generate based on the provided data.

<img width="400" alt="image" src="https://github.com/agupt295/AXIVision/assets/118144312/07e9f9e8-fefe-4d24-a080-5322ff99f120">
<img width="403" alt="image" src="https://github.com/agupt295/AXIVision/assets/118144312/01ac533f-a122-46c6-9f2b-b6c43a00e83f">

## Installation and Usage

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python 3.6 or later installed.
- You have `pip` installed.

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/agupt295/AXIVision.git

2. **Run the following command:**

   ```sh
   python final_dashboard.py


