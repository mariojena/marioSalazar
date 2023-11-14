document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Event listener for submit
  document.querySelector('#compose-form').addEventListener('submit', send_email);
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      const list = document.createElement('ul');
      list.className = "messages";
      //  Go through emails and get info
      emails.forEach(singleEmail =>{
        // First create the li element and set the class
        const li = document.createElement('li');
        if (singleEmail.read === true){
          li.className = "message";
        } else {
          li.className = "message unread";
        }
        li.setAttribute("id", `m${singleEmail.id}`);

        // Wrap everything in a <a>
        const a = document.createElement('a');

        // Create a div for icons unread or archive
        const actions = document.createElement('div');
        actions.className = "actions";

        // Create the icons
        const read = document.createElement('span');
        read.className = "action";
        const icon_read = document.createElement('i');
        icon_read.className = singleEmail.read ?  "fa fa-envelope-open" : "fa fa-envelope";
        icon_read.setAttribute("id", `i${singleEmail.id}`)
        read.append(icon_read);
        read.addEventListener('click', function() {
          bool_read(singleEmail.id)
        });
        actions.append(read);

        const arch = document.createElement('span');
        arch.className = "action";
        const icon_arch = document.createElement('i');
        icon_arch.className = singleEmail.archived?  "fa fa-archive text-primary" : "fa fa-archive";
        arch.append(icon_arch);
        arch.addEventListener('click', function() {
          bool_archived(singleEmail.id)
        });
        actions.append(arch);

        li.append(actions);

        // Create the div header and  set the class
        const header = document.createElement('div');
        header.className = "header";

        // Create the content of the div header and append thems
        const from = document.createElement('span');
        from.className = "from"
        from.innerHTML = `${singleEmail.sender}`;
        header.append(from);
        const date = document.createElement('span');
        date.className = "date"
        date.innerHTML = `${singleEmail.timestamp}`;
        header.append(date);

        // Append the header to <a>
        a.append(header);

        // Create the a div for the subject
        const subject = document.createElement('div');
        subject.className = "title";
        subject.innerHTML = `${singleEmail.subject}`;

        // Append the subject to the <a>
        a.append(subject);

        // Create a div for the body
        const body = document.createElement('div');
        body.className = "description";
        body.innerHTML = `${singleEmail.body}`;

        // Append the body to the a
        a.append(body);

        // Append the a to the li
        li.append(a);
        // Append the li to the ul (list)
        list.append(li);
        // Add a function redirect the user to a link when clicked
        a.addEventListener('click', function() {
            view_email(singleEmail.id)
        });
        document.querySelector('#emails-view').append(list);
      })
  });
}

function send_email(event) {
  event.preventDefault();
  // Take the fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Pass the data to compose.views
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      load_mailbox('sent');
  });
}

function view_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Hide the other view, so that only appears the email
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#single-email').style.display = 'block';

      // ... do something else with email ...

      // Create a div which class is "details"
      const details = document.createElement('div');
      details.className = "details";

      // Create a div for the subject
      const subject = document.createElement('div')
      subject.className = "title";
      subject.innerHTML = `${email.subject}`;

      // Append the subject to the details div
      details.append(subject);

      // Create an archive button and make it work
      const toolbar = document.createElement('div');
      toolbar.className = "toolbar";

      const btn_group = document.createElement('div');
      btn_group.className = "btn-group";

      const button = document.createElement('button');
      button.className = "btn btn-secondary";
      button.setAttribute("type", "button");

      const icon_arch = document.createElement('span');
      icon_arch.className = email.archived?  "fa fa-archive text-dark" : "fa fa-archive";
      icon_arch.innerHTML = email.archived?  " Unarchive" : " Archive";

      button.append(icon_arch)
      btn_group.append(button);
      toolbar.append(btn_group);

      button.addEventListener('click', function() {
        bool_archived(email.id)
      });

      // Create an reply button and make it work

      const button_re = document.createElement('button');
      button_re.className = "btn btn-primary";
      button_re.setAttribute("type", "button");

      const icon_re = document.createElement('span');
      icon_re.className = "fa fa-reply";
      icon_re.innerHTML = " reply";

      button_re.append(icon_re)
      btn_group.append(button_re);
      toolbar.append(btn_group);

      button_re.addEventListener('click', function() {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        // if (!email.subject.startsWith("Re:")){
        //   const new_sub = "Re: " + email.subject;
        //   console.log(new_sub);
        // }
        document.querySelector('#compose-subject').value = !email.subject.startsWith("Re:") ? "Re: " + email.subject: email.subject
        document.querySelector('#compose-body').value = `on ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      });

      // Create a div for the header
      const header = document.createElement('div');
      header.className = "header";

      // Create a div for the sender and timestamp
      const from = document.createElement('div');
      from.className = "from";
      from.innerHTML = `<span>from: ${email.sender}</span>`;

      // Create a p to the recipients
      const to = document.createElement('p');
      to.innerHTML = `To: ${email.recipients}`
      from.append(to);
      header.append(from);

      const date = document.createElement('div');
      date.className = "date";
      date.innerHTML = `<span>${email.timestamp}</span>`
      header.append(date);

      // Append the header to details
      details.append(header);

      // Create a div for the body
      const body = document.createElement('div');
      body.className = "content";
      body.innerHTML = `${email.body}`;
      details.append(body);

      // At the end. Remember to give a class of  message
      document.querySelector('#single-email').className = "message";
      document.querySelector('#single-email').innerHTML = "";
      document.querySelector('#single-email').append(toolbar);
      document.querySelector('#single-email').append(details);

      // Change read to true
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
  });
}

function bool_read(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: !email.read
        })
      })
      if (!email.read){
        document.querySelector(`#m${email.id}`).className = "message";
        document.querySelector(`#i${email.id}`).className = "fa fa-envelope-open";
      } else if (email.read){
        document.querySelector(`#m${email.id}`).className = "message unread";
        document.querySelector(`#i${email.id}`).className = "fa fa-envelope";
      }
  })
}

function bool_archived(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then(() => {email.archived ? load_mailbox('inbox'):load_mailbox('archive')})
  })
}