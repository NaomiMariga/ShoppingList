let current_list_name = undefined;
let current_list_id = undefined;

$('#signupForm').on('shown.bs.collapse', function () {
  // do something…
    $('#loginForm').collapse('hide');
    $('#pass_reset').collapse('hide');
});

$('#loginForm').on('shown.bs.collapse', function () {
    // execute
    $('#signupForm').collapse('hide');
    $('#pass_reset').collapse('hide');
});

$('#pass_reset').on('shown.bs.collapse', function () {
    $('#signupForm').collapse('hide');
    $('#loginForm').collapse('hide');

});

let login_page = document.querySelector("#loginPage");
let main_page = document.querySelector('#mainPage');

function login() {
    let email = document.querySelector("#login_email");
    let password = document.querySelector("#login_password");
    $.ajax({
        url: "login",
        type: "POST",
        data: {
            email : email.value,
            password: password.value
        },
        dataType: "json",
        success: function (response) {
            let element = document.querySelector("#login_alerts");
            if(response.success){
                email.value = "";
                password.value = "";
                window.sessionStorage.setItem("token", response.message.token);
                window.sessionStorage.setItem("user_id", response.message.user_id);
                window.sessionStorage.setItem("username", response.message.username);

                read_lists();
                login_page.classList.add('d-none');
                if(main_page.classList.contains('d-none')){
                    main_page.classList.remove('d-none');
                }

            }else{
                password.value = "";
                 Alert(response.message, element, true);
            }
        }
    })
}
function resetPassword() {
    let email = document.querySelector('#reset_email').value;
    $.ajax({
        url: "reset_password",
        type: "POST",
        data: {
            email: email
        },
        dataType: "json",
        success: function (response) {
          let element = document.querySelector("#reset_password_alerts");
          if(response.success){
              Alert(response.message,element,false)
          }else{
              Alert(response.message,element,true)
          }
        }
    })

}
function create_lists() {
    let new_list = document.querySelector("#new_list_name");
    let element = document.querySelector("#new_list_alerts");
    $.ajax({
        url: "shoppingList_create",
        type: "POST",
        data: {
            list_name: new_list.value,
            token: sessionStorage.getItem("token"),
            user_id:sessionStorage.getItem("user_id")

        },
        dataType: "json",
        success: function (response) {
            if(response.success){
                Alert(response.message,element,false);
                new_list.value = "";
                read_lists();
                // $("#new_list").modal('hide');
            }else {
                Alert(response.message, element, true)
            }

        },
        error: function (error) {
            Alert("An error occurred, please try again",element, true)
        }
    })
    
}

function change_password(){
    let cur_pass = document.querySelector("#current_pass");
    let new_pass = document.querySelector("#new_pass");
    let conf_pass = document.querySelector("#conf_pass");
    if(new_pass.value === conf_pass.value){
        $.ajax({
            url: "change_password",
            type: "POST",
            data: {
                new_password: new_pass.value,
                old_password: cur_pass.value,
                token: window.sessionStorage.getItem("token"),
                user_id: window.sessionStorage.getItem("user_id")
            },
            success: function (response) {
                if(response.success){
                cur_pass.value = "";
                new_pass.value = "";
                conf_pass.value = "";
                    Alert(response.message, document.querySelector("#change_pass_alerts"),false);
                }else{
                    Alert(response.message, document.querySelector("#change_pass_alerts"),true);
                }
            }
        });
    }else{
        Alert("Passwords do not match", document.querySelector("#change_pass_alerts"),true);
    }
}


function read_lists() {
   let my_lists = document.querySelector("#myLists");
    $.ajax({
        url: "read_lists",
        type: "POST",
        data:{
            token:sessionStorage.getItem("token"),
            user_id:sessionStorage.getItem("user_id"),

        }, 
        success: function (response) {
            if(response.success){
                /*
                <a href="#" class="list-group-item flex-column">
                    <div class="d-sm-flex w-100 justify-content-between">
                        <h6 class="mb-1">Back to School</h6>
                        <span class="small text-muted"></span>

                 */
                let lists = response.message;
                while(my_lists.hasChildNodes()){
                    my_lists.removeChild(my_lists.lastChild);
                }
                for(let key in lists) {
                    let list = lists[key];
                    let a = document.createElement("a");
                    a.setAttribute("onclick", "read_items("+list.list_id+",\""+list.list_name+"\")");
                    a.className = "list-group-item flex-column";
                    let div = document.createElement("div");
                    div.className = "d-sm-flex w-100 justify-content-between";
                    let h6 = document.createElement("h6");
                    h6.className = "mb-1";
                    let text = document.createTextNode(list.list_name);
                    h6.appendChild(text);
                    let span = document.createElement("span");
                    span.className = "small text-muted";
                    div.appendChild(span);
                    div.appendChild(h6);
                    a.appendChild(div);
                    my_lists.appendChild(a);
                    document.querySelector("#list_name").innerHTML = list.list_name;

                }
            }

        }
    });
}

function add_item() {
    $.ajax({
        url: "add_items",
        type:"POST",
        data:{
            token: window.sessionStorage.getItem("token"),
            user_id: window.sessionStorage.getItem("user_id"),
            list_id: current_list_id,
            item_name: "",
            quantity: "",
            units: "",
            cost: ""
        },
        success: function (response) {
            if(response.success){
                read_items(current_list_id,current_list_name);
            }

        }
    })

}

function update_item(list_id, item_id, attribute, value) {
    $.ajax({
        url: "edit_items",
        type: "POST",
        data: {
            list_id: list_id,
            item_id: item_id,
            attribute: attribute,
            value:value,
            user_id: window.sessionStorage.getItem("user_id"),
            token: window.sessionStorage.getItem("token")
        },
        success: function (response) {
            if(!response.success){
                alert(response.message);
            }
        }
    })

}

function read_items(list_id, list_name) {
    current_list_name = list_name;
    current_list_id = list_id;
    document.querySelector("#list_name").innerHTML = current_list_name;
    document.querySelector("#text_rename_list").value = current_list_name;
    document.querySelector("#text_delete_list").innerHTML = current_list_name;
    let list_items = document.querySelector("#list_items");
    $.ajax({
        url: "read_items",
        type: "POST",
        data:{
            user_id: sessionStorage.getItem("user_id"),
            token: sessionStorage.getItem("token"),
            list_id:list_id
        },success: function (response) {
            let items = response.message;
            while(list_items.hasChildNodes()){
                list_items.removeChild(list_items.lastChild);
            }
            for(let key in items){
                let item = items[key];
                let tr = document.createElement("tr");
                let td1 = document.createElement("td");
                let input_1 = document.createElement("input");
                input_1.type = "text";
                input_1.value = item.item_name;
                input_1.className = "form-control";
                input_1.setAttribute("placeholder", "Item");
                input_1.setAttribute("onchange","update_item("+list_id+", "+item.item_id+", 'item_name', this.value)");
                td1.appendChild(input_1);
                let td2 = document.createElement("td");
                let input_2 = document.createElement("input");
                input_2.type = "text";
                input_2.className = "form-control form-control-sm float-left quantity";
                input_2.setAttribute("onchange","update_item("+list_id+", "+item.item_id+", 'quantity', this.value)");
                input_2.setAttribute("placeholder", "Quantity");
                input_2.value = item.quantity;
                td2.appendChild(input_2);
                let input_3 = document.createElement("input");
                input_3.type = "text";
                input_3.className = "form-control form-control-sm float-right units";
                input_3.setAttribute("list", "units");
                input_3.setAttribute("placeholder", "");
                input_3.value = item.units;
                input_3.setAttribute("onchange","update_item("+list_id+", "+item.item_id+", 'units', this.value)");
                td2.appendChild(input_3);
                let td3 = document.createElement("td");
                let input_4 = document.createElement("input");
                input_4.type ="text";
                input_4.className = "form-control";
                input_4.setAttribute("placeholder", "Cost");
                input_4.setAttribute("title", "Cost per item");
                input_4.value = item.cost;
                input_4.setAttribute("onchange","update_item("+list_id+", "+item.item_id+", 'cost', this.value)");
                td3.appendChild(input_4);
                let td4 = document.createElement("td");
                let td5 = document.createElement("td");
                let a = document.createElement("a");
                a.className ="material material-minus-circle-outline text-danger";
                a.setAttribute("onclick", "delete_item("+item.item_id+", "+list_id+")");
                td5.appendChild(a);
                tr.appendChild(td1);
                tr.appendChild(td2);
                tr.appendChild(td3);
                tr.appendChild(td4);
                tr.appendChild(td5);
                list_items.appendChild(tr);

            }

        }
    })
    /*
    <tr>
        <td><input type="text" class="form-control" placeholder="Item"></td>
        <td>
            <input type="text" class="form-control form-control-sm float-left quantity"
                   placeholder="Quantity">
            <input type="text" class="form-control form-control-sm float-right units" list="units"
                   placeholder="">
        </td>
        <td><input type="text" class="form-control" placeholder="Cost" title="Cost per item"></td>
        <td>0.00</td>
        <td><a href="#!remove" class="material material-minus-circle-outline text-danger"></a></td>
    </tr>
     */
}

function edit_lists(list_id) {
    let text_rename_list = document.querySelector("#text_rename_list");
    let element = document.querySelector("#edit_list_alert");
    $.ajax({
        url: "edit_lists",
        type:"POST",
        data:{
            user_id:window.sessionStorage.getItem("user_id"),
            token: window.sessionStorage.getItem("token"),
            list_id:list_id,
            list_name:text_rename_list.value
        },
        success: function (response) {
            if(response.success){
                current_list_name = text_rename_list.value;
                read_lists()

            }else {
                Alert(response.message, element,true);
            }


        }
    })

}
function delete_lists(){
    let element = document.querySelector("#delete_list_alert");
    $.ajax({
        url: "delete_lists",
        type: "POST",
        data: {
            user_id: window.sessionStorage.getItem("user_id"),
            token: window.sessionStorage.getItem("token"),
            list_id: current_list_id
        },
        success: function (response) {
            if(response.success){
                let list_items = document.querySelector("#list_items");
                while (list_items.hasChildNodes()){
                    list_items.removeChild(list_items.lastChild);
                }

                current_list_name = undefined;
                current_list_id = undefined;
                document.querySelector("#list_name").innerHTML = "Your List Items goes here";
                document.querySelector("#text_rename_list").value = "";
                document.querySelector("#text_delete_list").innerHTML = "";
                $("#delete_list").modal('hide');
                read_lists();
            }else{
                read_lists();
                Alert(response.message,element,true);
            }

        }


    })

}
function delete_item(item_id, list_id) {
    let element = document.querySelector("#list_alerts");
    $.ajax({
        url: "delete_items",
        type: "POST",
        data: {
            item_id:item_id,
            list_id: list_id,
            user_id: window.sessionStorage.getItem("user_id"),
            token: window.sessionStorage.getItem("token")
        },
        success:function (response) {
            if(!response.success){
                Alert(response.message, element,true);
            }
            read_items(list_id, current_list_name);
        }
    })

}
function logout(){
    $.ajax({
        url: "logout",
        type: "POST",
        data: {
            user_id: window.sessionStorage.getItem("user_id"),
            token: window.sessionStorage.getItem("token")
        },
        dataType: "json",
        success: function(response) {
            window.sessionStorage.clear();
        }
    });
    main_page.classList.add('d-none');

    if (login_page.classList.contains('d-none')){
        login_page.classList.remove('d-none');

    }
}

let signup = function () {
    let email = document.querySelector("#registration_email");
    let username = document.querySelector("#username");
    let password = document.querySelector("#registration_password");
    $.ajax({
        url: "register",
        type: "POST",
        data: {
            email: email.value,
            username: username.value,
            password: password.value
        },
        dataType:"json",
        success: function (response) {
            let element = document.querySelector("#signup_alerts");
            if(response.success){
                Alert(response.message, element, false);
                email.value = "";
                username.value = "";
                password.value= "";
            }else{
                Alert(response.message, element, true);
            }
        },
        error: function (error) {
          Alert("An error occurred", element, false);
          console.log(error);
        }

    });
};

function menu(current, show){
    let shopping = document.querySelector("#shopping_page");
    let profile = document.querySelector("#myProfile");
    let menus = document.querySelectorAll(".nav-item");
    for(let key in menus){
        let menu = menus[key];
        menu.className = "nav-item";
    }
    current.className = "nav-item active";
    shopping.style.visibility = "hidden";
    profile.style.visibility = "hidden";
    document.querySelector(show).style.visibility = "visible";
}


function Alert(message, element, error)
{
    let close = document.createElement("button");
    close.setAttribute("type","button");
    close.classList.add("close");
    close.setAttribute("data-dismiss","alert");
    close.setAttribute("aria-label","Close");
    let span = document.createElement("span");
    span.setAttribute("aria-hidden","true");
    span.className = "material material-close-circle-o";
    close.appendChild(span);

    let div = document.createElement("div");
    let text = new Text(message);
    div.appendChild(close);
    div.appendChild(text);
    if(error){
        div.className = "alert alert-danger alert-dismissible fade show";
    }else{
        div.className = "alert alert-success alert-dismissible fade show";
    }
    div.setAttribute("role","alert");

    while (element.hasChildNodes()) {
        element.removeChild(element.lastChild);
    }
    element.appendChild(div);
    setTimeout(function () {
        element.removeChild(div);
    }, 6000);
}

