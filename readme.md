# Ray Tracing API 🌟

This is a university project that implements the graphic ray tracing algorithm in a simple way. I've enhanced the project by adding a Flask API, type hints, logging, and organizing its structure. Additionally, I've implemented a faster algorithm that uses a thread pool to run in parallel based on the CPU count. 🚀

To make it more user-friendly, I've integrated some GPT and prompt magic, allowing users to describe their 3D scene in natural language and receive an image back. This is a great feature because describing a full 3D scene purely by numbers can be challenging. 🎨

There's still a lot to improve in this project, such as optimizations to the algorithm, adding new objects, adding illuminated objects, and improving GPT to return more accurate scenes.

## Getting Started 🛠

To use the project, follow these steps:

1. Clone the repository to your desired folder:
   ```bash
   git clone https://github.com/Tomer-Lavan/ray-tracing.git
    ```
2. Install the required dependencies:
    ```bash
   pip install -r requirements.txt
    ``` 
3. Add your OpenAI key to .env.example and rename the file to .env.
4. Run the server:
   ```bash
   python server.py
    ```
5. Send a request to one of the two endpoints:
 - POST / - Body: { "message": "string" } (Description of the scene you want)
 - POST /fast - Body: { "message": "string" } (Faster algorithm)

 # Future Improvements 🔮 
 - Optimizations to the ray tracing algorithm such as Bounding Volume Hierarchies, Spatial Partitioning, Level of Detail (LOD) and Adaptive Sampling.
 - Adding support for new geometric objects.
 - Implementing illuminated objects.
 - Enhancing GPT integration for more accurate scene descriptions.
 - Feel free to contribute to this project and make it even better! 🌈

 # Project Examples
 -  ![Example 1](https://github.com/Tomer-Lavan/ray-tracing/main/images/example1.png)
 -  ![Example 2](https://github.com/Tomer-Lavan/ray-tracing/main/images/example2.png)

