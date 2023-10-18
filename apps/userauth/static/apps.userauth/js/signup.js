const input = document.querySelector('#phone');

        input.addEventListener('input', function(event) {
             if (this.value.length >= 9){
                this.classList.remove("is-invalid");
                this.classList.add("is-valid");
             } else {
                this.classList.remove("is-valid");
                this.classList.add("is-invalid");
             };
        });