const mentorData = document.getElementById("mentor-data");
const mentorList = document.getElementById("mentor-list");

const branch = mentorData.dataset.branch;
const category = mentorData.dataset.category;

async function loadMentors() {
  mentorList.innerHTML = '<div class="loading-card">Loading mentors...</div>';

  try {
    const response = await fetch(`/get_mentors?branch=${branch}&category=${category}`);
    const mentors = await response.json();

    if (mentors.length === 0) {
      mentorList.innerHTML = `
        <div class="loading-card">
          No mentors found for this branch and category.
        </div>
      `;
      return;
    }

    mentorList.innerHTML = mentors.map((mentor) => `
      <article class="mentor-card">
        <img src="${mentor.photo}" alt="${mentor.name}">

        <div class="mentor-info">
          <h2>${mentor.name}</h2>
          <p><strong>Email:</strong> ${mentor.email}</p>
          <p><strong>Phone:</strong> ${mentor.phone}</p>
        </div>
      </article>
    `).join("");
  } catch (error) {
    mentorList.innerHTML = `
      <div class="loading-card">
        Unable to load mentors. Please try again.
      </div>
    `;
  }
}

loadMentors();
