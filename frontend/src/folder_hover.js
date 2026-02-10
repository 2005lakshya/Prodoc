import React from 'react';
import './folder_hover.css';

const Card = () => {
    return (
        <section className="folder-card-section">
            <div className="folder-file-wrapper">
                <div className="folder-work-5" />
                <div className="folder-work-4" />
                <div className="folder-work-3" />
                <div className="folder-work-2" />
                <div className="folder-work-1" />
            </div>
            <p className="folder-text">Drag & Drop Here</p>
        </section>
    );
}

export default Card;
