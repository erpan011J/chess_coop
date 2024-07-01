import axios from 'axios';
import { useUserStore } from '@/stores/userStore';

const baseURL = 'http://localhost:8000/api';

const axiosInstance = axios.create({
    baseURL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

const getErrorMessage = (error) => {
    if (error.response.data) {
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

const updateUserStore = (username, roomName) => {
    const userStore = useUserStore();
    userStore.setUserName(username);
    userStore.setRoomName(roomName);
};

export const createRoom = async (roomName, username) => {
    try {
        // Send data to backend to handle Redis storage
        const response = await axiosInstance.post('/rooms/', {
            name: roomName,
            username,
        });
        let { room_name } = response.data; // Extract room_name from response
        updateUserStore(username, roomName); // Update local user store
        return room_name; // Return room_name upon success
    } catch (error) {
        const errorMessage = getErrorMessage(error);
        throw new Error(errorMessage);
    }
};

export const joinRoom = async (roomName, username) => {
    try {
        // Send data to backend to handle Redis storage
        const response = await axiosInstance.post(`/rooms/${roomName}/join/`, {
            username,
        });

        let { room_name } = response.data; // Extract room_name from response
        updateUserStore(username, roomName); // Update local user store
        return room_name; // Return room_name upon success
    } catch (error) {
        const errorMessage = getErrorMessage(error);
        throw new Error(errorMessage);
    }
};

export default axiosInstance;
