/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import Product from "./form/Product";

export default function Home() {
  const [user, setUser] = useState({});
  const [isAdmin, setIsAdmin] = useState(false);
  const [products, setProducts] = useState([]);
  const [tableHead, setTableHead] = useState([
    "no",
    "id",
    "description",
    "title",
    "vendor",
    "created_at",
    "modified",
    "status",
    "image"
  ]);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const handleApprove = (id) => {
    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;
    axios
      .post(`http://localhost:8000/products/${id}/approve`, {}, {
        headers: { Authorization: token },
      })
      .then((response) => {
        getProducts();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const getProducts = () => {
    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;

    axios
      .get("http://localhost:8000/products/", {
        headers: { Authorization: token },
      })
      .then((response) => {
        setProducts(response.data.result);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    // get token from local storage
    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;

    //  fetch data from get user api
    axios
      .get("http://localhost:8000/users/", {
        headers: { Authorization: token },
      })
      .then((response) => {
        setUser(response.data.result);
        const isAdminUser = response.data.result.roles.some((role) => role.role_name === "admin");
        setIsAdmin(isAdminUser);
      })
      .catch((error) => {
        console.log(error);
      });

      getProducts();

  }, []);


  const tdTable = (data) => {
    const td_list = [];
    let index = 0
    for (const [key, value] of Object.entries(data)) {
      if (key === "image_data") {
        td_list.push(<td key={index}><img src={`data:image/jpeg;base64,${value}`} alt={`Image ${index + 1}`} width="50" /></td>);
      } else if (key === "image") {
        continue
      } else {
        td_list.push(<td key={index}>{value}</td>);
      }

      index+=1
    }
    return td_list;
  };


  const handleProductCreated = (newProduct) => {
    getProducts();
  };

  return (
    <div className="bg-gray-200 font-sans h-screen w-full flex flex-col">
      <div className="shadow rounded border-b border-gray-200">
          <div className="overflow-x-auto">
            {/* Table Data */}
            <table className="table table-zebra w-full">
              <thead>
                <tr>
                  {tableHead.map((data, index) => {
                    return (
                      <th className="cursor-pointer" key={index}>
                        {data}
                      </th>
                    );
                  })}
                </tr>
              </thead>
              <tbody>
                {products.map((data, index) => {
                   return (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      {tdTable(data)}
                      <td>{ isAdmin && <button onClick={()=> handleApprove(data.id)} className="py-2 px-4 mt-4 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">APPROVE</button> } </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

             {/* Button to open the modal */}
            <button
              onClick={openModal}
              className="py-2 px-4 mt-4 bg-gray-500 hover:bg-gray-600 text-white rounded-lg"
            >
              Create New Product
            </button>

            {/* Overlay and Modal for creating a new product */}
            {isModalOpen && (
            <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
              <Product user={user} closeModal={closeModal} onProductCreated={handleProductCreated} />
            </div>
             )}
          </div>
      </div>
    </div>
  );
}
