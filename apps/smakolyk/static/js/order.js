// IDK how to make it work with Django (I mean to import it from another file), so I just put it here
const DataMappingValues = Object.freeze({
    dish_quantity_field_names: [
        "first_course_quantity",
        "second_course_quantity",
        "dessert_quantity",
        "drink_quantity"
    ],
    dish_price_field_names: [
        "first_course_price",
        "second_course_price",
        "dessert_price",
        "drink_price"
    ],
    dish_field_names: [
        "first_course",
        "second_course",
        "dessert",
        "drink"
    ],
})

let monday_form, tuesday_form, wednesday_form, thursday_form, friday_form;
let all_day_divs = [];

for (let i = 1; i < 6; i++) {
    all_day_divs.push(document.getElementById(`subform${i}`))
}

[monday_form, tuesday_form, wednesday_form, thursday_form, friday_form] = all_day_divs;

let amount_div_1, amount_div_2, amount_div_3, amount_div_4, amount_div_5;
let all_amount_divs = []

for (let i = 1; i < 6; i++) {
    all_amount_divs.push(document.getElementById(`div-grn${i}`))
}

[amount_div_1, amount_div_2, amount_div_3, amount_div_4, amount_div_5] = all_amount_divs;

let save_button = document.getElementById('save');

function activateDiv(element) {
    let days = document.getElementsByClassName("list");

    for(let day of days){
        day.classList.remove("active");
    }

    element.classList.add("active");

    for(let day of all_day_divs){
        day.classList.remove("on");

        if (day.id.slice(-1) === element.id.slice(-1)){
            day.classList.add("on");
        }
    }

    for (let amount of all_amount_divs) {
        if (!amount.classList.contains("off")) {
            amount.classList.add("off");
        }

        if (amount.id.slice(-1) === element.id.slice(-1)) {
            amount.classList.remove("off");
        }
    }

    if (element.id.slice(-1) === "5") {
        save_button.style.visibility = "visible";
    } else {
        save_button.style.visibility = "hidden";
    }

}

let all_dish_prices;

function getCSRFToken() {
    return document.getElementsByName('csrfmiddlewaretoken')[0].value;
}

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/set-price/');
        const data = await response.json();
        all_dish_prices = data.response;

    } catch (error) {
        alert("Dish prices are not available. Please, try again later.");
    }
});

function get_total_amount(form_number) {
    let form_data = {};

    for (const field_name of DataMappingValues.dish_quantity_field_names) {
        let result_value = parseInt(document.getElementById(`id_form-${form_number}-${field_name}`).value);

        if (isNaN(result_value)) {
            result_value = 0;
        }
        form_data[field_name] = result_value;
    }

    for (const [index, field_name] of DataMappingValues.dish_price_field_names.map(
                (value, index) => [index, value]
            )
        ) {
        let result_value = parseInt(
            all_dish_prices[
                DataMappingValues.dish_field_names[index]][
                    document.getElementById(`id_form-${form_number}-${DataMappingValues.dish_field_names[index]}`).value
                ]
        );

        if (isNaN(result_value)) {
            result_value = 0;
        }
        form_data[field_name] = result_value;
    }

    return fetch('/set-total-price/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(form_data)
    })
    .then(response => response.json())
    .then(data => {
        return data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function set_first_sourse_select_options(
    first_course_select, first_course_price, fist_course_quantity, currency_amount, form_number
) {
    first_course_select.addEventListener('change', () => {
        if (first_course_select.value === "") {
            first_course_price.innerHTML = "<p>0</p>";
            fist_course_quantity.value = 0;

        } else if (parseInt(fist_course_quantity.value) > 0) {
            first_course_price.innerHTML = "<p>" + (parseInt(fist_course_quantity.value) * parseInt(all_dish_prices['first_course'][first_course_select.value])) + "</p>";

            get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
            });

        } else {
            first_course_price.innerHTML = "<p>0</p>";
            fist_course_quantity.value = 0;
        }
    });
}

function set_first_course_quantity_options(first_course_select, first_course_price, fist_course_quantity, currency_amount, form_number) {
    fist_course_quantity.addEventListener('change', () => {
       if (first_course_select.value === "------") {
           first_course_price.innerHTML = "<p>0</p>";

       } else if (first_course_select.value) {
           first_course_price.innerHTML = "<p>" + (parseInt(fist_course_quantity.value) * parseInt(all_dish_prices['first_course'][first_course_select.value])) + "</p>";

           get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
            });

       } else {
           first_course_price.innerHTML = "<p>0</p>";
       }
    });
}

function set_second_sourse_select_options(second_course_select, second_course_price, second_course_quantity, currency_amount, form_number) {
    second_course_select.addEventListener('change', () => {
        if (second_course_select.value === "") {
            second_course_price.innerHTML = "<p>0</p>";
            second_course_quantity.value = 0;
        } else if (parseInt(second_course_quantity.value) > 0) {
            second_course_price.innerHTML = "<p>" + (parseInt(second_course_quantity.value) * parseInt(all_dish_prices['second_course'][second_course_select.value])) + "</p>";

            get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
            });
        } else {
            second_course_price.innerHTML = "<p>0</p>";
            second_course_quantity.value = 0;
        }
    });
}

function set_second_course_quantity_options(second_course_select, second_course_price, second_course_quantity, currency_amount, form_number) {
    second_course_quantity.addEventListener('change', () => {
       if (second_course_select.value === "------") {
           second_course_price.innerHTML = "<p>0</p>";

       } else if (second_course_select.value) {
           second_course_price.innerHTML = "<p>" + (parseInt(second_course_quantity.value) * parseInt(all_dish_prices['second_course'][second_course_select.value])) + "</p>";

           get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
           });

       } else {
           second_course_price.innerHTML = "<p>0</p>";
       }
    });
}

function set_dessert_select_options(dessert_select, dessert_price, dessert_quantity, currency_amount, form_number) {
    dessert_select.addEventListener('change', () => {
        if (dessert_select.value === "") {
            dessert_price.innerHTML = "<p>0</p>";
            dessert_quantity.value = 0;
        } else if (parseInt(dessert_quantity.value) > 0) {
            dessert_price.innerHTML = "<p>" + (parseInt(dessert_quantity.value) * parseInt(all_dish_prices['dessert'][dessert_select.value])) + "</p>";

            get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
            });
        } else {
            dessert_price.innerHTML = "<p>0</p>";
            dessert_quantity.value = 0;
        }
    });
}

function set_dessert_quantity_options(dessert_select, dessert_price, dessert_quantity, currency_amount, form_number) {
    dessert_quantity.addEventListener('change', () => {
       if (dessert_select.value === "------") {
           dessert_price.innerHTML = "<p>0</p>";

       } else if (dessert_select.value) {

           dessert_price.innerHTML = "<p>" + (parseInt(dessert_quantity.value) * parseInt(all_dish_prices['dessert'][dessert_select.value])) + "</p>";

           get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
           });

       } else {
           dessert_price.innerHTML = "<p>0</p>";
       }
    });
}

function set_drink_select_options(drink_select, drink_price, drink_quantity, currency_amount, form_number) {
    drink_select.addEventListener('change', () => {
        if (drink_select.value === "") {
            drink_price.innerHTML = "<p>0</p>";
            drink_quantity.value = 0;
        } else if (parseInt(drink_quantity.value) > 0) {
            drink_price.innerHTML = "<p>" + (parseInt(drink_quantity.value) * parseInt(all_dish_prices['drink'][drink_select.value])) + "</p>";

            get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
            });
        } else {
            drink_price.innerHTML = "<p>0</p>";
            drink_quantity.value = 0;
        }
    });
}

function set_drink_quantity_options(drink_select, drink_price, drink_quantity, currency_amount, form_number) {
    drink_quantity.addEventListener('change', () => {
       if (drink_select.value === "------") {
            drink_price.innerHTML = "<p>0</p>";

       } else if (drink_select.value) {
           drink_price.innerHTML = "<p>" + (parseInt(drink_quantity.value) * parseInt(all_dish_prices['drink'][drink_select.value])) + "</p>";

           get_total_amount(form_number).then(data => {
                if (data.amount_deducted) {
                    alert("You overcame the limit. The difference will be deducted from your salary.");
                }

                currency_amount.textContent = data.response;
           });

       } else {
           drink_price.innerHTML = "<p>0</p>";
       }
    });
}

for (let i = 0; i <= 5; i++) {
    let total_amount = document.getElementById(`grn${i + 1}`);

    const first_course_price = document.getElementById(`form${i + 1}_first_course_price`);
    const fist_course_quantity = document.getElementById(`id_form-${i}-first_course_quantity`);
    const first_course_select = document.getElementById(`id_form-${i}-first_course`);

    // setting event listeners for first course divs related
    set_first_sourse_select_options(first_course_select, first_course_price, fist_course_quantity, total_amount, i);
    set_first_course_quantity_options(first_course_select, first_course_price, fist_course_quantity, total_amount, i);

    const second_course_price = document.getElementById(`form${i + 1}_second_course_price`);
    const second_course_quantity = document.getElementById(`id_form-${i}-second_course_quantity`);
    const second_course_select = document.getElementById(`id_form-${i}-second_course`);

    // setting event listeners for second course divs related
    set_second_sourse_select_options(second_course_select, second_course_price, second_course_quantity, total_amount, i);
    set_second_course_quantity_options(second_course_select, second_course_price, second_course_quantity, total_amount, i);

    const dessert_price = document.getElementById(`form${i + 1}_dessert_price`);
    const dessert_quantity = document.getElementById(`id_form-${i}-dessert_quantity`);
    const dessert_select = document.getElementById(`id_form-${i}-dessert`);

    // setting event listeners for dessert divs related
    set_dessert_select_options(dessert_select, dessert_price, dessert_quantity, total_amount, i);
    set_dessert_quantity_options(dessert_select, dessert_price, dessert_quantity, total_amount, i);

    const drink_price = document.getElementById(`form${i + 1}_drink_price`);
    const drink_quantity = document.getElementById(`id_form-${i}-drink_quantity`);
    const drink_select = document.getElementById(`id_form-${i}-drink`);

    // setting event listeners for drink divs related
    set_drink_select_options(drink_select, drink_price, drink_quantity, total_amount, i);
    set_drink_quantity_options(drink_select, drink_price, drink_quantity, total_amount, i);

}
