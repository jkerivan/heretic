import "./App.css";
import React, { useState, useEffect } from "react";
import Forgot from "./form/Forgot";
import Login from "./form/Login";
import Register from "./form/Register";
import Home from "./Home";
import { toast } from "react-toastify";


function App() {
  const [page, setPage] = useState("login");
  const [token, setToken] = useState();

  useEffect(() => {
    const auth = localStorage.getItem("auth_token");
    setToken(auth);
  }, [token]);

  const chosePage = () => {
    if (page === "login") {
      return <Login setPage={setPage} />;
    }
    if (page === "forgot") {
      return <Forgot setPage={setPage} />;
    }
    if (page === "register") {
      return <Register setPage={setPage} />;
    }
  };

  const onClickHandler = (event) => {
    event.preventDefault();

    // remove token form local storage
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_token_type");

    toast("See You !", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });

    // reload page
    setTimeout(() => {
      window.location.reload();
    }, 1500);
  };

  const pages = () => {
    if (token == null) {
      return (
        <div className="min-h-screen bg-gray-400 flex justify-center items-center">
          <div className="py-12 px-12 bg-white rounded-2xl shadow-xl z-20">
            {chosePage()}
          </div>
        </div>
      );
    } else {
      return <Home />;
    }
  };

  return (
    <React.Fragment>
      <nav className="bg-gray-600 p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h2 className="text-xl font-semibold text-white">Uncle Bill's Surfs Shop</h2>
          <button
            onClick={(event) => {
              onClickHandler(event);
            }}
            className="py-2 px-4 text-white text-sm bg-gray-800 hover:bg-gray-700 active:bg-gray-900 rounded-lg"
          >
            Log out
          </button>
        </div>
      </nav>

      {pages()}
    </React.Fragment>
  );
}

export default App;
