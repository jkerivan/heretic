import React, { useState } from "react";
import axios from "axios";

export default function Product({ user, closeModal, onProductCreated }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState(null);

  const handleClose = async (event) => {
    event.preventDefault();
    closeModal();
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;

    const formData = new FormData();
    formData.append("image", image);
    formData.append("title", title);
    formData.append("description", description);
    formData.append("vendor_id", user.vendor_id);

    try {
      const response = await axios.post("http://0.0.0.0:8000/products/", formData, {
        headers: { Authorization: token },
      });
      onProductCreated(response.data.result);
      setTitle("");
      setDescription("");
      setImage(null);
      closeModal();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <React.Fragment>
      <div>
        <h2 className="text-3xl font-bold text-center mb-4"> Add New Product</h2>
        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <div className="mt-6">
            <div className="space-y-4">
              <input type="text" 
                    placeholder="Title"
                    value={title} onChange={(e) => setTitle(e.target.value)} 
                    required
                    className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-black-400"
              
              />
            </div>
          </div>

          <div className="mt-6">
            <div className="space-y-4">
              <textarea 
                value={description}
                placeholder="Description"
                onChange={(e) => setDescription(e.target.value)} 
                required 
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-black-400"
                />
            </div>
          </div>
          <label>Select an image:</label>
          <input
            type="file"
            accept="image/*"
            name="image"
            onChange={(e) => setImage(e.target.files[0])}
            className="block mt-4"
          />

          <div className="mt-6">
            <button
              className="py-3 w-64 text-xl text-black bg-gray-400 rounded-2xl hover:bg-black-300 active:bg-black-500 outline-none"
              type="submit">Create Product</button>
              <button onClick={handleClose}
              className="py-3 w-64 text-xl text-black bg-gray-400 rounded-2xl hover:bg-black-300 active:bg-black-500 outline-none"
              type="submit">Close</button>
          </div>
        </form>
      </div>
    </React.Fragment>
  );
    
    
}
