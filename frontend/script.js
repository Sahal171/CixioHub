async function login() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    const formData =
        new URLSearchParams();

    formData.append(
        "username",
        email
    );

    formData.append(
        "password",
        password
    );

    const response = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
            method: "POST",
            headers: {
                "Content-Type":
                "application/x-www-form-urlencoded"
            },
            body: formData
        }
    );

    const data =
        await response.json();

    if(data.access_token){

        localStorage.setItem(
            "token",
            data.access_token
        );

        document.getElementById(
            "result"
        ).innerText =
            "Login Successful";

    } else {

        document.getElementById(
            "result"
        ).innerText =
            "Login Failed";
    }
}


async function getProfile() {

    const token =
        localStorage.getItem("token");

    if(!token){
        alert("Please login first");
        return;
    }

    const response = await fetch(
        "http://127.0.0.1:8000/auth/me",
        {
            headers: {
                Authorization:
                `Bearer ${token}`
            }
        }
    );

    const data =
        await response.json();

    document.getElementById(
        "profile"
    ).innerHTML = `
        <h3>User Profile</h3>
        <p>Name: ${data.name}</p>
        <p>Email: ${data.email}</p>
    `;
}


async function getNotes() {

    const token =
        localStorage.getItem("token");

    if(!token){
        alert("Please login first");
        return;
    }

    const response = await fetch(
        "http://127.0.0.1:8000/notes",
        {
            headers: {
                Authorization:
                `Bearer ${token}`
            }
        }
    );

    const notes =
        await response.json();

    let output =
        "<h3>Notes</h3>";

    notes.forEach(note => {

        output += `
            <div>
                <h4>${note.title}</h4>
                <p>${note.content}</p>
                <p><b>Tags:</b> ${note.tags}</p>
                <hr>
            </div>
        `;
    });

    document.getElementById(
        "notes"
    ).innerHTML = output;
}


async function createNote() {

    const token =
        localStorage.getItem("token");

    if(!token){
        alert("Please login first");
        return;
    }

    const title =
        document.getElementById("title").value;

    const content =
        document.getElementById("content").value;

    const tags =
        document.getElementById("tags").value;

    const response = await fetch(
        "http://127.0.0.1:8000/notes",
        {
            method: "POST",

            headers: {
                "Content-Type":
                "application/json",

                Authorization:
                `Bearer ${token}`
            },

            body: JSON.stringify({
                title: title,
                content: content,
                tags: tags
            })
        }
    );

    const data =
        await response.json();

    alert("Note Created Successfully");

    getNotes();
}