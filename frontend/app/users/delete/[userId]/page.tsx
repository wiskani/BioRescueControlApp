"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';

//React imports
import {
    useEffect,
    useCallback,
    useState
}  from 'react';

//Api imports
import {
    DeleteUserApi,
    GetUserById
} from "@/app/libs/users/ApiUsers"

export default function DeleteUser({ params} : { params: { userId: number } }) {
    const { data: session } = useSession();
    const user = session?.user;
    const [userIdData, setUserIdData] = useState<UsersResponseData | null>(null);

    const userData = useCallback(
        async (): Promise<UsersResponseData>=> {
            if (user) {
                try {
                    const data = await GetUserById({
                        token: user?.token,
                        id: params.userId
                    });
                    return data;
                } catch (error) {
                    if (error instanceof Error) {
                        console.error(error.message);
                        throw error;
                    }
                    throw error;
                }

            }
            throw new Error('User not found');
        }, [user, params.userId]);

    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
        else {
            userData().then((data) => {
                setUserIdData(data);
            });
        }
    }, [session, userData]);


    return (
        <div>
            <h1>Delete User</h1>
            <p>Are you sure you want to delete this user?</p>
            <p>{userIdData?.name}</p>
            <p>{userIdData?.email}</p>
        </div>
    );
}

