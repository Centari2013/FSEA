import { directoryEntityCardFactory } from "../utility";
import { cardContainer } from "../search/cardTemplates";
import { titleCard } from "./directoryCardTemplates";

export function createAlphabeticDirectory(entities, sortKey, entityType, directoryTitle) {
    const mainContentArea = document.getElementById('main-content');

    // Clear existing contents and setup new structure
    const depTitleCard = titleCard(directoryTitle);
    mainContentArea.innerHTML = '';
    const titleCardContainer = cardContainer();
    titleCardContainer.innerHTML += depTitleCard;
    mainContentArea.appendChild(titleCardContainer);
    mainContentArea.innerHTML += `
        <div id="alphabet-navigation" class="alphabet-nav"></div>
        <div id="directory-container"></div>
    `;

    

    const alphabetNavContainer = document.getElementById('alphabet-navigation');
    const directoryContainer = document.getElementById('directory-container');

    // Normalize and sort entities
    const normalizedEntities = entities.map(entity => ({
        ...entity,
        sortValue: entity[sortKey].replace(/^the /i, '') // Ignore "The" at the beginning
    })).sort((a, b) => a.sortValue.localeCompare(b.sortValue));

    // Determine unique starting letters for navigation
    const letters = new Set(normalizedEntities.map(entity => entity.sortValue[0].toUpperCase()));

    // Create alphabet navigation links
    letters.forEach(letter => {
        const link = document.createElement('a');
        link.textContent = letter;
        link.href = `#section-${letter}`;
        link.onclick = (e) => {
            e.preventDefault();
            const targetSection = document.getElementById(`section-${letter}`);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        };
        alphabetNavContainer.appendChild(link);
    });

    // Create directory content for each letter
    letters.forEach(letter => {
        const section = document.createElement('div');
        section.id = `section-${letter}`;
        section.classList.add('entity-section', 'row', 'row-cols-1', 'g-4', 'justify-content-center');
        section.innerHTML = `<h2>${letter}</h2>`;

        const filteredEntities = normalizedEntities.filter(entity => entity.sortValue.startsWith(letter));
        filteredEntities.forEach(entity => {
            section.innerHTML += directoryEntityCardFactory(entity, entityType);
        });

        directoryContainer.appendChild(section);
    });
}



