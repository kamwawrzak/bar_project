document.getElementById('upload-photo').addEventListener('change', ()=>{
   let file = document.getElementById('upload-photo').files[0];
   document.getElementById('up-photo-label').innerHTML = file.name.substring(0, 15) + '...';
   let img = document.getElementById('img-display');
   if (img) { img.src = URL.createObjectURL(file); };
});