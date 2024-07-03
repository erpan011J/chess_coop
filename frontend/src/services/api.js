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
    if (error.response && error.response.data) {
        const responseData = error.response.data;
        for (let key in responseData) {
            if (Array.isArray(responseData[key])) {
                return `${responseData[key][0]}`;
            } else {
                return `${responseData[key]}`;
            }
        }
        return 'Unknown error occurred';
    } else {
        return 'Network error occurred';
    }
};

const updateLocalStorage = (userName, roomName) => {
    localStorage.setItem('userName', userName);
    localStorage.setItem('roomName', roomName);
};

export const createRoom = async (roomName, userName) => {
    try {
        // Send data to backend to handle Redis storage
        const response = await axiosInstance.post('/rooms/', {
            name: roomName,
            username: userName,
        });
        let { room_name } = response.data; // Extract room_name from response
        updateLocalStorage(userName, roomName); // Update local storage
        return room_name; // Return room_name upon success
    } catch (error) {
        const errorMessage = getErrorMessage(error);
        throw new Error(errorMessage);
    }
};

export const joinRoom = async (roomName, userName) => {
    try {
        // Send data to backend to handle Redis storage
        const response = await axiosInstance.post(`/rooms/${roomName}/join/`, {
            username: userName,
        });

        let { room_name } = response.data; // Extract room_name from response
        updateLocalStorage(userName, roomName); // Update local storage
        return room_name; // Return room_name upon success
    } catch (error) {
        const errorMessage = getErrorMessage(error);
        throw new Error(errorMessage);
    }
};

export const fetchInitialRoomData = async (roomName, userName) => {
    try {
        const response = await axiosInstance.post(`/rooms/${roomName}/initial_data/`, {
            username: userName,
        });
        return response.data;
    } catch (error) {
        console.log(error)
        const errorMessage = getErrorMessage(error);
        throw new Error(errorMessage);
    }
};

export default axiosInstance;
