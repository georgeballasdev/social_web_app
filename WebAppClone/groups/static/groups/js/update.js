const imgInput = document.querySelector('#id_img');
const preview = document.querySelector('#preview');

imgInput.onchange = () => {
    const [file] = imgInput.files
    if (file) {
        preview.src = URL.createObjectURL(file);
    }  
  }