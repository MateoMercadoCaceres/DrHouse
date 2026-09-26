def generate_medicine_image_prompt(medicine_name: str, description: str | None = None) -> str:
    base_prompt = (
        f'Create a professional 3D rendered image of a medicine bottle/package for {medicine_name}. '
        'The image should show both the medicine container and the medicine itself. '
        'Include clear labeling and professional pharmaceutical packaging design. '
        'Use a clean, medical aesthetic with appropriate colors for a pharmaceutical product. '
        'The image should be suitable for medical documentation and professional use.'
    )
    
    if description:
        base_prompt += f' Additional details: {description}'
        
    return base_prompt
