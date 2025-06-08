// Sorting button logic for view page

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.smallFilterButton');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            const sort = btn.getAttribute('data-sort');
            const dir = btn.getAttribute('data-dir');
            const url = new URL(window.location.href);
            // Remove all sort params first
            const sortFields = ['word', 'isFromBeginning', 'counts', 'hashType', 'user', 'createdAt'];
            sortFields.forEach(f => url.searchParams.delete(f));
            url.searchParams.set(sort, dir);
            window.location.href = url.pathname + url.search;
        });
    });
});
