const addBox = document.querySelector(".add-box"),
    popupBox = document.querySelector(".popup-box"),
    popupTitle = popupBox.querySelector("header p"),
    closeIcon = popupBox.querySelector("header i"),
    titleTag = popupBox.querySelector("input"),
    descTag = popupBox.querySelector("textarea"),
    addBtn = popupBox.querySelector("button");

const months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];

document.addEventListener("DOMContentLoaded", () => {
  showNotes();
});

let global_note_id = 0;

addBox.addEventListener("click", () => {
    popupTitle.innerText = "ADD NOTE";
    addBtn.innerText = "ADD";
    popupBox.classList.add("show");
    document.querySelector("body").style.overflow = "hidden";
    if (window.innerWidth > 660) titleTag.focus();
});

closeIcon.addEventListener("click", () => {
    titleTag.value = descTag.value = "";
    popupBox.classList.remove("show");
    document.querySelector("body").style.overflow = "auto";
});


function showNotes() {
    fetch("/notes")
        .then(response => response.json())
        .then(notes => {
            if (!notes) return;
            document.querySelectorAll(".note").forEach(li => li.remove());
            notes.forEach((note) => {
                global_note_id = note.id;
                let filterDesc = note.description.replaceAll("\n", '<br/>');
                let liTag = `<li class="note">
                                <div class="details">
                                    <p>${note.title}</p>
                                    <span>${filterDesc}</span>
                                </div>
                                <div class="bottom-content">
                                    <span>${note.date}</span>
                                    <div class="settings">
                                        <i onclick="showMenu(this)" class="uil uil-ellipsis-h"></i>
                                        <ul class="menu">
                                            <li onclick="editNote(${note.id})"><i class="uil uil-pen"></i>Edit</li>
                                            <li onclick="deleteNote(${note.id})"><i class="uil uil-trash"></i>Delete</li>
                                        </ul>
                                    </div>
                                </div>
                            </li>`;
                addBox.insertAdjacentHTML("afterend", liTag);
            });
        })
        .catch(error => {
            console.error("Error retrieving notes:", error);
        });
}

showNotes();



function showMenu(elem) {
    elem.parentElement.classList.add("show");
    document.addEventListener("click", e => {
        if (e.target.tagName != "I" || e.target != elem) {
            elem.parentElement.classList.remove("show");
        }
    });
}



function deleteNote(noteId) {
    let confirmDel = confirm("Are you sure you want to delete this note?");
    if(!confirmDel) return;
    fetch(`/notes/${noteId}`, {
        method: "DELETE"
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            showNotes();
        });
}


addBtn.addEventListener("click", e => {
    e.preventDefault();
    let title = titleTag.value.trim();
    let description = descTag.value.trim();

    if (title || description) {
        let currentDate = new Date();
        let month = months[currentDate.getMonth()];
        let day = currentDate.getDate();
        let year = currentDate.getFullYear();

        let data = {
            title: title,
            description: description,
            date: `${month} ${day}, ${year}`
        };

        // Check if the popupTitle contains "Update" to determine if it's an update or add action
        if (popupTitle.innerText.includes("Update")) {
            // If it's an update, call the updateNote function
            updateNote(data);
        } else {
            // If it's an add, call the addNote function
            addNote(data);
        }
    }
});

function editNote(noteId) {
    fetch(`/notes/${noteId}`)
        .then(response => response.json())
        .then(note => {
            titleTag.value = note.title;
            descTag.value = note.description;
            popupTitle.innerText = "Update a Note";
            addBtn.innerText = "Update Note";
            popupBox.classList.add("show");
            document.querySelector("body").style.overflow = "hidden";
            if (window.innerWidth > 660) titleTag.focus();
      });
}


function addNote(data) {
    fetch("/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(newNote => {
            console.log(newNote);
            showNotes();
            closeIcon.click();
        });
}


function updateNote(data) {
    let noteId = global_note_id;

    fetch(`/notes/${noteId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(updatedNote => {
            console.log(updatedNote);
            showNotes();
            closeIcon.click();
        });
}