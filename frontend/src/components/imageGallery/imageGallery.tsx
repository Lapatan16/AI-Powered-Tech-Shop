import React, { useState } from 'react';
import './ImageGallery.css';

interface ImageGalleryProps {
  images: string[];
  productName: string;
}

export const ImageGallery: React.FC<ImageGalleryProps> = ({ images, productName }) => {
  const [activeIndex, setActiveIndex] = useState<number>(0);

  const fallbackImage = 'https://placehold.co/400x400?text=No+Image+Available&font=roboto';
  
  if (!images || images.length === 0) {
    return (
      <div className="image-gallery-fallback">
        <img src={fallbackImage} alt={productName} />
      </div>
    );
  }

  const handlePrev = () => {
    setActiveIndex((prev) => (prev === 0 ? images.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setActiveIndex((prev) => (prev === images.length - 1 ? 0 : prev + 1));
  };

  return (
    <div className="image-gallery-container">
      <div className="image-gallery-viewer">
        <img src={images[activeIndex]} alt={`${productName} view ${activeIndex + 1}`} />
        
        {images.length > 1 && (
          <>
            <button className="gallery-control btn-prev" onClick={handlePrev} aria-label="Previous image">
              &#10094;
            </button>
            <button className="gallery-control btn-next" onClick={handleNext} aria-label="Next image">
              &#10095;
            </button>
          </>
        )}
      </div>

      {images.length > 1 && (
        <div className="image-gallery-thumbnails">
          {images.map((imgUrl, index) => (
            <button
              key={index}
              className={`thumbnail-track-btn ${index === activeIndex ? 'active' : ''}`}
              onClick={() => setActiveIndex(index)}
            >
              <img src={imgUrl} alt={`${productName} thumbnail ${index + 1}`} />
            </button>
          ))}
        </div>
      )}
    </div>
  );
};