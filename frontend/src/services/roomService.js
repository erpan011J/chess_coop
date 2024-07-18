import axios from 'axios';

const baseURL = 'http://localhost:8000/api';

const axiosInstance = axios.create({
    baseURL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

const getErrorMessage = (error) => {
    if (error.response) {
        if (error.response.data && error.response.data.error) {
            return error.response.data.error;
        }
        return error.response.data || error.response.statusText || 'An error occurred';
    } else if (error.request) {
        return 'No response received from server';
    } else {
        return error.message || 'An unexpected error occurred';
    }
};

const updateLocalStorage = (userName, roomName) => {
    localStorage.setItem('userName', userName);
    localStorage.setItem('roomName', roomName);
};

export const createRoom = async (roomName, userName) => {
    try {
        const response = await axiosInstance.post('/rooms/', {
            name: roomName,
            username: userName,
        });
        updateLocalStorage(userName, roomName);
        return response.data;
    } catch (error) {
        throw new Error(getErrorMessage(error));
    }
};

export const joinRoom = async (roomName, userName) => {
    try {
        const response = await axiosInstance.post(`/rooms/${roomName}/join/`, {
            username: userName,
        });
        updateLocalStorage(userName, roomName);
        return response.data;
    } catch (error) {
        throw new Error(getErrorMessage(error));
    }
};

export const fetchInitialRoomData = async (roomName, userName) => {
    try {
        const response = await axiosInstance.post(`/rooms/${roomName}/initial_data/`, {
            username: userName,
        });
        return response.data;
    } catch (error) {
        throw new Error(getErrorMessage(error));
    }
};

export default axiosInstance;
