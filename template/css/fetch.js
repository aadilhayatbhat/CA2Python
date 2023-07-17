// // Function to fetch and display data from API
// function fetchData(apiUrl, containerId) {
//     fetch(apiUrl)
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById(containerId).textContent = data;
//         })
//         .catch(error => {
//             console.log('Error:', error);
//         });
// }




// Function to fetch and display data from API
function fetchData(apiUrl, containerId, processFunction) {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            processFunction(data, containerId);
        })
        .catch(error => {
            console.log('Error:', error);
        });
}

//displaying student data

function displayStudents(data, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = ''; // Clear the container before adding new content

    data.forEach(student => {
        const studentInfo = document.createElement('div');
        studentInfo.textContent = `ID: ${student.student_id}, Name: ${student.student_name}, Email: ${student.student_email}`;
        container.appendChild(studentInfo);
    });
}

//displaying category data
function displayCategories(data, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = ''; // Clear the container before adding new content

    data.forEach(category => {
        const categoryInfo = document.createElement('div');
        categoryInfo.textContent = `Category ID: ${category.category_id}, Category Name: ${category.category_name}`;
        container.appendChild(categoryInfo);
    });
}

// // Example usage for displaying book data
// function displayBooks(data, containerId) {
//     const container = document.getElementById(containerId);
//     container.innerHTML = ''; // Clear the container before adding new content

//     data.forEach(book => {
//         const bookInfo = document.createElement('div');
//         bookInfo.textContent = `Book ID: ${book.book_id}, Title: ${book.title}, Author: ${book.author}`;
//         container.appendChild(bookInfo);
//     });
// }



// Fetch and display students
fetchData('http://127.0.0.1:5000/students', 'studentTable', displayStudents);

// Fetch and display categories
fetchData('http://127.0.0.1:5000/categories', 'categoryTable', displayCategories);

// Fetch and display books
fetchData('http://127.0.0.1:5000/books', 'bookContainer', displayBooks);


// // Fetch data
// fetchData('http://127.0.0.1:5000/categories', 'categoryTable');

// // Fetch data
// fetchData('http://127.0.0.1:5000/students', 'studentTable');