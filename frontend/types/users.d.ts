export {};

declare global {
    interface UsersResponseData{
        id: number; 
        email: string;
        permissions: string[];
        name: string;
        last_name: string;
    }

}


