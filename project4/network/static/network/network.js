document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#dropDownUser').addEventListener('click', () => dropdown());
    document.querySelector('#click_post').addEventListener('click', () => add_post());
    document.querySelector('#close_post').addEventListener('click', () => close_post());

    // Event listener to expand the inputs}
    document.querySelector('#location').addEventListener('focus', () => expand('location'));
    document.querySelector('#img_url').addEventListener('focus', () => expand('img_url'));

    // Shrink the inputs if it is empty
    document.querySelector('#location').addEventListener('blur', () => shrink('location'));
    document.querySelector('#img_url').addEventListener('blur', () => shrink('img_url'));

    // Event listening for showing the dropdown of a comment
    let dropdowns = document.querySelectorAll('a[id|="dropdown"]');
    for (let i=0; i<dropdowns.length; i++){
      dropdowns[i].addEventListener('click', () => dropdown_show(dropdowns[i].id))
    }

    // Event listening for showing the dropdown of a comment
    let dropdownsc = document.querySelectorAll('a[id|="dropdownc"]');
    for (let i=0; i<dropdownsc.length; i++){
      dropdownsc[i].addEventListener('click', () => dropdown_show(dropdownsc[i].id))
    }

    // Event Listener for adding a comment
    let listAddComment = document.querySelectorAll('button[id|="addcomment"]')
    for (let i=0; i<listAddComment.length; i++){
      listAddComment[i].addEventListener('click', ()=> add_comment(listAddComment[i].id));
    }

    // Event listener for liking a post
    let listLikePost = document.querySelectorAll('button[id|="likepost"]')
    for (let i=0; i<listLikePost.length; i++){
      listLikePost[i].addEventListener('click', ()=> add_likepost(listLikePost[i].id));
    }

    // Event listener for liking a comment
    let listLikeComment = document.querySelectorAll('button[id|="likecomment"]')
    for (let i=0; i<listLikeComment.length; i++){
      listLikeComment[i].addEventListener('click', ()=> add_likecomment(listLikeComment[i].id));
    }

    // Event Listener for editing a post
    let listEditPost = document.querySelectorAll('li[id|="edit"]')
    for (let i=0; i<listEditPost.length; i++){
      listEditPost[i].addEventListener('click', ()=> edit_post(listEditPost[i].id));
    }

    // Event Listener for accepting a request
    let listAccept = document.querySelectorAll('button[id|="accept"]')
    for (let i=0; i<listAccept.length; i++){
      listAccept[i].addEventListener('click', ()=> accept_request(listAccept[i].id));
    }

    // Event Listener for unfollowing a person
    let listDeleteFollower = document.querySelectorAll('button[id|="delete"]')
    for (let i=0; i<listDeleteFollower.length; i++){
      listDeleteFollower[i].addEventListener('click', ()=> delete_request(listDeleteFollower[i].id));
    }

    // Event listener for sending a Request
    let btnSend = document.querySelector('button[id|="send"]');
    if (btnSend) {
      btnSend.addEventListener('click', ()=> send_request(btnSend.id), {once:true});
    }

    // Event Listener for unfollowing a person
    let btnDelete = document.querySelector('button[id|="deletep"]');
    if (btnDelete) {
      btnDelete.addEventListener('click', ()=> delete_request(btnDelete.id));
    }

    // Event Listener for deleting a follow request
    let btnDeleter = document.querySelector('button[id|="deleter"]');
    if (btnDeleter) {
      btnDeleter.addEventListener('click', ()=> delete_request(btnDeleter.id));
    }

    // Event Listener for deleting a post
    let listDeletePost = document.querySelectorAll('li[id|="deletepost"]')
    for (let i=0; i<listDeletePost.length; i++){
      listDeletePost[i].addEventListener('click', ()=> delete_element(listDeletePost[i].id));
    }

    // Event Listener for deleting a commment
    let listDeleteComment = document.querySelectorAll('li[id|="deletec"]')
    for (let i=0; i<listDeleteComment.length; i++){
      listDeleteComment[i].addEventListener('click', ()=> delete_element(listDeleteComment[i].id));
    }

});

// Function for displaying the dropdown next to the username's at the left down side
function dropdown(){
  if (document.querySelector('#dropdown-profile').style.display === 'block'){
    document.querySelector('#dropdown-profile').style.display = '';
  } else {
    document.querySelector('#dropdown-profile').style.display = 'block';
  }
}

// Function for displaying the post form
function add_post(){
  document.querySelector('#add-post').classList.add("show");
}

// Function for closing the form of a new post
function close_post(){
  document.querySelector('#add-post').classList.remove("show");
  document.querySelector('#edit-post').classList.remove("show");
}

// Function for giving the animation to the inputs Where and photo
function expand(input_exp){
  document.querySelector(`#${input_exp}`).style.animationName = 'expand';
  document.querySelector(`#${input_exp}`).style.animationPlayState = 'running';
}

// Function for reverting the animations of the add_post form
function shrink(input_shrink){
  if (document.querySelector(`#${input_shrink}`).value === "") {
    document.querySelector(`#${input_shrink}`).style.animationName = 'shrink';
    document.querySelector(`#${input_shrink}`).style.animationPlayState = 'running';
  }

  document.querySelector(`#${input_shrink}`).animationPlayState = 'paused';
}

// Function for showing the droplist of comments and posts
function dropdown_show(list){
  let [type, id] = list.split("-");
  if (type === "dropdown"){
    let droplist = document.querySelector(`#droplist-${id}`);
    droplist.classList.toggle("show");
  } else {
    let droplist = document.querySelector(`#droplistc-${id}`);
    droplist.classList.toggle("show");
  }
}

// Function for adding a comment
function add_comment(id){
  id = id.slice(11);
  const textarea = document.querySelector(`#contentcomment-${id}`);
  content = textarea.value;

  // Send the data to the backend
  fetch('/comment', {
    method: 'POST',
    body: JSON.stringify({
        content: content,
        post_id: id
    })
  })
  .then(response => response.json())
  .then(comment_new => {
    comment_new = comment_new[0];
    // Select the ul tag where all the comments are wraped
    let ul = document.querySelector(`#commentspost${id}`);

    // Create the list item for the comment
    const li = document.createElement('li');
    li.className = "comment-item w-100";

    // Div for all
    const allDiv = document.createElement('div');
    allDiv.className = "d-flex position-relative";

    // Create the div for Avatar
    const divAvatar = document.createElement('div');
    divAvatar.className = "avatar avatar-xs";

    // Create the link and the avatar
    const aAvatar = document.createElement('a');
    aAvatar.setAttribute("href", "#!");
    // Must add the profile
    const imgAvatar = document.createElement('img');
    imgAvatar.className = "avatar-img rounded-circle";
    imgAvatar.setAttribute("src", comment_new.profile_photo);
    imgAvatar.setAttribute("alt", `Profile Photo of ${capitalize(comment_new.username)}`);

    // Append the link and avatar to the div
    aAvatar.append(imgAvatar);
    divAvatar.append(aAvatar);
    allDiv.append(divAvatar);

    // Create a div for the username and the content
    const divContent = document.createElement('div');
    divContent.className = "bg-light rounded-start-top-0 p-3 rounded";

    // Create a div for the username
    const divUsername = document.createElement('div');
    divUsername.className = "d-flex justify-content-between";

    // Create an h6 for the username
    const h6 = document.createElement('h6');
    h6.className = "mb-1";

    // Create an a element for username
    const aUsername = document.createElement('a');
    aUsername.setAttribute("href", "#!"); // Must change the link
    aUsername.innerHTML = `${capitalize(comment_new.username)}`

    // Create a div element that wraps username, content and reaction
    const div2 = document.createElement('div');
    div2.className = "ms-2 w-100";

    // Create an element for date
    const date = document.createElement('small');
    date.className = "ms-2";
    date.innerHTML = `${comment_new.date}`

    // Wrap the username in to the div
    h6.append(aUsername);
    divUsername.append(h6);
    divUsername.append(date);
    div2.append(divUsername)

    // Create a p element for the content
    const p = document.createElement('p');
    p.className = "small mb-0";
    p.innerHTML = comment_new.content

    // Wrap into the divContent
    divContent.append(divUsername);
    divContent.append(p);
    div2.append(divContent);

    // Create a div for the reactions
    const likeUl = document.createElement('ul');
    likeUl.className = "nav nav-divider py-2 small";

    // Create a li for the like reaction
    const likeLi = document.createElement('li');
    likeLi.className = 'nav-item';

    // Create an a an the icon
    const aLike = document.createElement('a');
    aLike.className = "nav-link text-secondary";
    aLike.setAttribute("href", "!#"); // Must change
    aLike.innerHTML = ' <i class="bi bi-hand-thumbs-up-fill pe-1"></i> Like '

    // Wrap the elements of the reaction div
    likeLi.append(aLike);
    likeUl.append(likeLi);
    div2.append(likeUl);
    allDiv.append(div2)

    // Append everthing to the list
    li.append(allDiv);
    ul.prepend(li);
    textarea.value = "";
  })
}

// Function for adding or removing the like of the post
function add_likepost(id){
  // Send to the backend the id of post which like was clicked
  fetch('/like_post', {
    method: 'POST',
    body: JSON.stringify({
        post_id: id.slice(9)
    })
  })
  .then(response => response.json())
  .then(send => {
    send = send[0];
    // Once the like was added or removed to the post, update in the frontend
    const button = document.querySelector(`#${id}`);
    // Update the count of likes
    const countl = send.likes.length;
    // If like is 0, don't display any number, otherwise, display the number
    if (countl === 0){
      document.querySelector(`#countp-${id.slice(9)}`).innerHTML = "";
    } else {
      document.querySelector(`#countp-${id.slice(9)}`).innerHTML = countl;
    }
    // Check if the user is in the like list of the post
    if (send.likes.includes(send.user)){
      // If it is, start the animation
      button.classList.add("like-anim");
      button.style.animationPlayState = 'running';
      button.addEventListener('animationend', () => {
        button.classList.remove("like");
        button.classList.remove("like-anim");
        button.classList.add("liked");
    });
    } else {
      // Just turn the like to grey color
      button.classList.remove("liked");
      button.classList.add("like");
    }
  })
}

// Function for adding or removing the like of the comment
function add_likecomment(id){
  // Send to the backend the id of the comment which like was clicked
  fetch('/like_comment', {
    method: 'POST',
    body: JSON.stringify({
        comment_id: id.slice(12)
    })
  })
  .then(response => response.json())
  .then(send => {
    // Once the like was added or removed to the comment, update in the frontend
    send = send[0];
    const button = document.querySelector(`#${id}`);
    const countl = send.likes.length;
    const countp = document.querySelector(`#countc-${id.slice(12)}`);
    // If like is 0, don't display any number, otherwise, display the number
    countp.innerHTML = countl > 0? countl: "";
    // Check if the user is in the like list of the post
    if (send.likes.includes(send.user)){
      button.classList.add("like-anim");
      button.style.animationPlayState = 'running';
      button.addEventListener('animationend', () => {
        button.classList.remove("like");
        button.classList.remove("like-anim");
        button.classList.add("liked");
    });
    } else {
      // Just turn the like to grey color
      button.classList.remove("liked");
      button.classList.add("like");
    }
  })
}

// Function for editing a post
function edit_post(id){
  // Display the form for editing the post
  document.querySelector('#edit-post').classList.add("show");
  // Select the inputs of the form
  const location = document.querySelector('#locationedit');
  const img_url = document.querySelector('#img_urledit');
  const description = document.querySelector('#descriptionedit');
  const private = document.querySelector('#privateedit');
  // Select the div of the footer for the form
  let div_btn = document.querySelector('#footer-edit');
  // Create the input button
  let edit_button = document.createElement('input');
  edit_button.setAttribute("type", "button");
  edit_button.setAttribute("id", `edit_btn-${id.slice(5)}`);
  edit_button.className = "btn btn-primary";
  edit_button.setAttribute("value", 'Edit');
  // Append the button to the div
  div_btn.append(edit_button);
  // Get the close button

  const close_btn = document.querySelector(`#close_edit`);

  // Function for cleaning the data
  const close = function() {
    // Don't show the modal box
    document.querySelector('#edit-post').classList.remove("show");
    edit_button.removeEventListener('click', update);
    edit_button.remove()
  };

  // Fetch to get the information
  fetch('/edit_getpost', {
    method: 'POST',
    body: JSON.stringify({
        post_id: id.slice(5)
    })
  })
  // After getting the info, add to the value of each input
  .then(response => response.json())
  .then(post => {
    post = post[0];
    location.value = post.location;
    img_url.value = post.img_url;
    description.value = post.description;
    private.checked = post.private;
  })
    // Create the function for updating th data in the db
    const update = function() {
      // When clicked update the db
      fetch('/edit_post', {
        method: 'POST',
        body: JSON.stringify({
            post_id: id.slice(5),
            location: location.value,
            img_url: img_url.value,
            description: description.value,
            private:private.checked
        })
      })
      .then(response => response.json())
      .then(post => {
        post = post[0];
        // Select the existing post location in the page
        let postlocation = document.querySelector(`#location${id.slice(5)}`);
        // If the API of the post contains a location, add it or change the actual
        if (post.location){
          // If the location exists, just change the innerHTML
          if (postlocation){
            postlocation.innerHTML = `
            <input class="d-none" name="q" type="search" value="${post.location}"></a><button class="nav-item small ml-2 border-0 bg-transparent text-info" type="submit">${post.location}</button>
            `;
          } else {
            // Create the fiv and the form for accessing the location link
            let divlocation = document.querySelector(`#divlocation${id.slice(5)}`);
            let formloc = document.createElement('form');
            formloc.setAttribute("action", "https://www.google.com/search");
            formloc.setAttribute("method", "get");
            formloc.setAttribute("id", `location${id.slice(5)}`);
            formloc.innerHTML = `
            <input class="d-none" name="q" type="search" value="${post.location}"></a><button class="nav-item small ml-2 border-0 bg-transparent text-info" type="submit">${post.location}</button>
            `;
            divlocation.append(formloc);
          }
        } else {
          // But if the post location existed and not anymore, just delete it
          if (postlocation){
            postlocation.remove();
          }
        }

        // Select the post description and change the innerHTML to the new one
        let postdescription = document.querySelector(`#descriptionp${id.slice(5)}`);
        postdescription.innerHTML = `${post.description}`;

        // Select the old img element
        let postimage = document.querySelector(`#img${id.slice(5)}`);
        // If ther is an img in the post API. Then add it or change it
        if (post.img_url ) {
          // If there was an image in the old post, change the source
          if (postimage){
            postimage.setAttribute('src', post.img_url);
          } else {
            // If there wasn't an image, create an img, append it to the div of the image
            let divimg = document.querySelector(`#container${id.slice(5)}`);
            postimage = document.createElement('img');
            postimage.className = "card-img";
            postimage.setAttribute("src", post.img_url);
            postimage.setAttribute("id", `img${id.slice(5)}`);
            divimg.append(postimage);
          }
        } else {
          // If there is no image in the new API, remove it if there was
          if (postimage){
            postimage.remove();
          }
        }
      })
      close();
    };
    edit_button.addEventListener('click', update);
    close_btn.addEventListener('click', close)
}

// Function for accepting the request for following
function accept_request(reference){
  const [type, id] = reference.split('-');
  // Send to the back end the id of the request that was accepted
  fetch('/accept_request', {
    method: 'POST',
    body: JSON.stringify({
        request_id: id
    })
  })
  .then(response => response.json())
  .then(petition => {
    // Get the new request status
    petition = petition[0];
    // Select the text to say now that the request was accepted
    const parragraph = document.querySelector(`#state${id}`);
    parragraph.innerHTML = 'follows you now.';
    // Remove the accept button, no longer needed
    const acceptbtn = document.querySelector(`#accept-${id}`);
    acceptbtn.remove();
    // Change the text of the reject button
    const deletebtn = document.querySelector(`#delete-${id}`);
    deletebtn.innerHTML = "Delete from Followers"
  })
}

// Function for deleting the request follow
function delete_request(reference){
  const [type, id] = reference.split('-');
  // Send to the backend the request that was accepted
  fetch('/delete_request', {
    method: 'POST',
    body: JSON.stringify({
        request_id: id
    })
  })
  .then(response => response.json())
  .then(message => {
    // Check if the delete request came from a profile page or notifications
    if (type === "deletep"){
      // From page but was already a friend
      let btn = document.querySelector(`#${reference}`);
      btn.innerHTML =  '<i class="bi bi-check-lg pe-1"></i> Unfollow Succesfull';
      btn.className = "btn btn-info me-2";
    } else if(type === "deleter"){
      // From page but was waiting for a request acceptance
      let btn = document.querySelector(`#${reference}`);
      btn.innerHTML =  '<i class="bi bi-check-lg pe-1"></i> Request deleted';
      btn.className = "btn btn-info me-2";
    } else {
      // From the notifications
      const parragraph = document.querySelector(`#state${id}`);
      parragraph.innerHTML = message;
      const deletebtn = document.querySelector(`#delete-${id}`);
      deletebtn.remove();
    }
  })
}

// Send a request
function send_request(btn){
  const [type, id] = btn.split("-");
  // Send to the backend id of the user to follow
  fetch('/send_request', {
    method: 'POST',
    body: JSON.stringify({
        to_user_id: id
    })
  })
  .then(response => response.json())
  .then(petition => {
    // When the info was obtained, change the text to say that is accepted
    const btn_new = document.querySelector(`#${btn}`);
    btn_new.innerHTML =  '<i class="bi bi-check-lg pe-1"></i> Request sent';
    btn_new.setAttribute("id", `deletep-${petition[0].id}`);
    btn_new.className = "btn btn-success me-2";
  })
}

// Function for deleteing posts or comments
function delete_element(element){
  const [type, id] = element.split("-");
  fetch('/delete_element', {
    method: 'POST',
    body: JSON.stringify({
        id: id,
        type: type
    })
  })
  .then(response => response.json())
  .then(context => {
    if (type === "deletepost"){
      const postdelete = document.querySelector(`#post-${id}`);
      postdelete.classList.add("deleteanim");
      postdelete.style.animationPlayState = 'running';
      postdelete.addEventListener('animationend', () => {
        postdelete.remove();
        });
    } else {
      const commentdelete = document.querySelector(`#comment-${id}`);
      commentdelete.classList.add("deleteanim");
      commentdelete.style.animationPlayState = 'running';
      commentdelete.addEventListener('animationend', () => {
        commentdelete.remove();
        });
    }
  })
}

// Fucntion for capitalizing words
function capitalize(name){
  let first = name.charAt(0);
  first = first.toUpperCase();
  return(first + name.slice(1))
}