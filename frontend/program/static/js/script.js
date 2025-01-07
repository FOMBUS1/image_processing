function chek_isInt(value) {
    if (value!== "") {
        if (!isNaN(value)) {
            if (Number.isInteger(Number(value))) {
                const numX = parseInt(value, 10);
                if (numX > 0) {
                    return false
                }
                alert("Значения должны быть больше 0.");
                return true;
            }
            alert("Значения должны быть целыми числами.");
            return true;
        }
        alert("Значения должны быть числом.");
        return true;
    }
    alert("Поля не должны быть пустыми.");
    return true;
}

async function uploadFile(type_func) {
    const fileInput = document.getElementById('file-input');
    const previewImage = document.getElementById('previewImage');
    const modal = document.getElementById('previewModal');

    let angle = 0;

    if (fileInput.files.length === 0) { 
        alert("Пожалуйста, выберите картинку.");
        return;
    }
    if (type_func === 3) {
        var x_input = document.getElementById('xInput');
        var y_input = document.getElementById('yInput');
        if (chek_isInt(x_input.value) || chek_isInt(y_input.value)) {
            return;
        }
        var size = [parseInt(x_input.value), parseInt(y_input.value)];
    } else {
        var size = [0, 0];
    }

    if (type_func === 1) {
        let angleInput = document.getElementById('angleInput');
        angle = parseInt(angleInput.value)
    }

    var formData = new FormData();
    var type_func_int = parseInt(type_func);
    formData.append('file', fileInput.files[0]);
    console.log(fileInput.files[0]);
    formData.append('type_func', type_func_int);
    console.log(type_func_int);
    console.log('all correct 1');
    size.forEach((value) => {
        formData.append('size', value);
        console.log(value);
    });
    console.log('all correct 2');
    console.log(angle); 
    formData.append('angle', angle);
    console.log('all correct 3');
    console.log(formData);
    var response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });
    console.log('all correct 4');
    var jsonData = await response.json();
    previewImage.src = jsonData.image;
    const modalInstance = new bootstrap.Modal(modal, {
        keyboard: false
    });
    console.log('all correct 5');
    modalInstance.show();
}