function saveUser(email, password, name) {
    if (!email || !password || !name) {
        alert("All fields are required!");
        return;
    }
    let users = JSON.parse(localStorage.getItem("users")) || [];
    if (users.find(user => user.email === email)) {
        alert("User already exists!");
        return;
    }
    users.push({ email, password, name });
    localStorage.setItem("users", JSON.stringify(users));
    alert("Registration successful!");
}

// Retrieve user details
function getUser(email) {
    let users = JSON.parse(localStorage.getItem("users")) || [];
    return users.find(user => user.email === email);
}

// Save job postings with validation
function saveJob(title, description, budget, poster) {
    if (!title || !description || !budget) {
        alert("All fields are required!");
        return;
    }
    let jobs = JSON.parse(localStorage.getItem("jobs")) || [];
    jobs.push({ title, description, budget, poster });
    localStorage.setItem("jobs", JSON.stringify(jobs));
    loadJobs();
}

// Load jobs dynamically
function loadJobs(searchTerm = "") {
    let jobs = JSON.parse(localStorage.getItem("jobs")) || [];
    let jobList = document.getElementById("jobList");
    if (jobList) {
        jobList.innerHTML = "";
        jobs.filter(job => job.title.toLowerCase().includes(searchTerm.toLowerCase()))
            .forEach(job => {
                let li = document.createElement("li");
                li.className = "list-group-item";
                li.textContent = `${job.title} - $${job.budget} (Posted by: ${job.poster})`;
                jobList.appendChild(li);
            });
    }
}

// Save freelancer profiles with validation
function saveFreelancer(name, skills, email) {
    if (!name || !skills || !email) {
        alert("All fields are required!");
        return;
    }
    let freelancers = JSON.parse(localStorage.getItem("freelancers")) || [];
    freelancers.push({ name, skills, email });
    localStorage.setItem("freelancers", JSON.stringify(freelancers));
    loadFreelancers();
}

// Load freelancer profiles with filtering
function loadFreelancers(searchTerm = "") {
    let freelancers = JSON.parse(localStorage.getItem("freelancers")) || [];
    let freelancerList = document.getElementById("freelancerList");
    if (freelancerList) {
        freelancerList.innerHTML = "";
        freelancers.filter(freelancer => freelancer.skills.toLowerCase().includes(searchTerm.toLowerCase()))
            .forEach(freelancer => {
                let li = document.createElement("li");
                li.className = "list-group-item";
                li.textContent = `${freelancer.name} - Skills: ${freelancer.skills}`;
                freelancerList.appendChild(li);
            });
    }
}

// Event listeners for form submissions
document.getElementById("jobForm")?.addEventListener("submit", function(event) {
    event.preventDefault();
    let title = document.getElementById("jobTitle").value;
    let description = document.getElementById("jobDescription").value;
    let budget = document.getElementById("jobBudget").value;
    let poster = "Anonymous"; // Replace with logged-in user later
    saveJob(title, description, budget, poster);
});

document.getElementById("freelancerForm")?.addEventListener("submit", function(event) {
    event.preventDefault();
    let name = document.getElementById("freelancerName").value;
    let skills = document.getElementById("freelancerSkills").value;
    let email = document.getElementById("freelancerEmail").value;
    saveFreelancer(name, skills, email);
    loadFreelancers();
});

// Search functionality
document.getElementById("jobSearch")?.addEventListener("input", function(event) {
    loadJobs(event.target.value);
});

document.getElementById("freelancerSearch")?.addEventListener("input", function(event) {
    loadFreelancers(event.target.value);
});

document.addEventListener("DOMContentLoaded", () => {
    loadJobs();
    loadFreelancers();
});