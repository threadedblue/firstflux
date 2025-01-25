import fluxultra  # Replace with the actual FluxUltra library import
from PIL import Image

def run_fluxultra(prompt, input_image_path, output_image_path, strength=0.75, guidance_scale=7.5, steps=50):
    """
    Runs FluxUltra with a prompt and input image (image-to-image).

    Args:
        prompt (str): The text prompt to guide the image generation.
        input_image_path (str): Path to the input image.
        output_image_path (str): Path to save the generated image.
        strength (float): How much the output deviates from the input image (default: 0.75).
        guidance_scale (float): How closely the result follows the prompt (default: 7.5).
        steps (int): Number of denoising steps (default: 50).

    Returns:
        None: Saves the generated image to the output path.
    """
    # Load the input image
    input_image = Image.open(input_image_path).convert("RGB")

    # Initialize the FluxUltra pipeline
    pipeline = fluxultra.ImageToImagePipeline.from_pretrained("fluxultra-model")

    # Run the image-to-image generation
    result = pipeline.generate(
        prompt=prompt,
        init_image=input_image,
        strength=strength,
        guidance_scale=guidance_scale,
        steps=steps,
    )

    # Save the output image
    result.save(output_image_path)
    print(f"Generated image saved to {output_image_path}")


# Example usage
if __name__ == "__main__":
    prompt = "A futuristic city at sunset with glowing lights"
    input_image_path = "input.jpg"  # Replace with your input image file
    output_image_path = "output.jpg"  # Replace with the desired output file path

    run_fluxultra(prompt, input_image_path, output_image_path)
