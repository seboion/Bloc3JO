// SEB : MAJ du total à payer
function updateTotal() {
    let total = 0;
    document.querySelectorAll('.quantity').forEach(function(input) {
        const price = parseFloat(input.dataset.price);
        const quantity = parseInt(input.value) || 0;
        total += price * quantity;
    });
    document.getElementById('totalPrice').innerText = total.toFixed(2) + ' €';
}
// SEB : ajuste la quantité en utilisant les boutons + et -
function adjustQuantity(id, delta) {
    const input = document.getElementById('quantity-' + id);
    let newValue = (parseInt(input.value) || 0) + delta;
    if (newValue < 0) newValue = 0;
    input.value = newValue;
    updateTotal();
}


// SEB : Cache le menu pour les versions mobiles
function toggleMenu() {
    const menu = document.querySelector('.mobile-menu');
    const nav = document.querySelector('nav ul');
    menu.classList.toggle('open');
    nav.classList.toggle('open');
}

// SEB : ne recharge pas toutes la page pour les pages de simple consultation depuis /home
document.addEventListener('DOMContentLoaded', function() {
    const billetsLink = document.querySelector('a[href="/billets/"]'); // AJAX offres de billet
    const evenementsLink = document.querySelector('a[href="/evenements/"]'); // AJAX offres de billet


 
    //Ajax offres de billet
    if (billetsLink) {
        billetsLink.addEventListener('click', function(event) {
            event.preventDefault(); // Empêche le chargement complet de la page

            // requête AJAX
            fetch('/billets/')
                .then(response => response.text())
                .then(html => {
                    // Remplace le contenu de la section MAIN
                    document.querySelector('main').innerHTML = html;
                })
                .catch(error => console.error('Erreur lors du chargement de la page :', error));
        });
    }

        //Ajax visualisation des events
        if (evenementsLink) {
            evenementsLink.addEventListener('click', function(event) {
                event.preventDefault(); // Empêche le chargement complet de la page
    
                // requête AJAX
                fetch('/evenements/')
                    .then(response => response.text())
                    .then(html => {
                        // Remplace le contenu de la section MAIN
                        document.querySelector('main').innerHTML = html;
                    })
                    .catch(error => console.error('Erreur lors du chargement de la page :', error));
            });
        }
    



        
        
});
