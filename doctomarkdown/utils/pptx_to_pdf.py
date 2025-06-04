import os
import comtypes.client

def convert_pptx_to_pdf(input_path, output_folder_path):
    if os.path.isdir(input_path):
        # Input path is a directory
        input_folder_path = os.path.abspath(input_path)

        if not os.path.isdir(input_folder_path):
            print("Error: Input folder does not exist.")
            return

        input_file_paths = [os.path.join(input_folder_path, file_name) for file_name in os.listdir(input_folder_path)]
    else:
        # Input path is a file
        input_file_paths = [os.path.abspath(input_path)]

    # Use the input_file_path's directory if output_folder_path is not provided
    if not output_folder_path:
        output_folder_path = os.path.dirname(input_file_paths[0])

    output_folder_path = os.path.abspath(output_folder_path)

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    success_count = 0
    error_count = 0

    for input_file_path in input_file_paths:
        if not input_file_path.lower().endswith((".ppt", ".pptx")):
            continue

        try:
            # Create PowerPoint application object
            powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
            slides = powerpoint.Presentations.Open(input_file_path, WithWindow=False)
            file_name = os.path.splitext(os.path.basename(input_file_path))[0]
            output_file_path = os.path.join(output_folder_path, file_name + ".pdf")

            if os.path.exists(output_file_path):
                print(f"Error: Output file '{output_file_path}' already exists.")
                error_count += 1
                continue

            # Save as PDF (formatType = 32)
            slides.SaveAs(output_file_path, 32)

            # Close the slide deck
            slides.Close()

            powerpoint.Quit()

            success_count += 1
        except Exception as e:
            print(f"Error converting file '{input_file_path}': {str(e)}")
            error_count += 1

    print(f"Conversion completed: {success_count} files converted successfully, {error_count} files failed.")
