import { useSession } from "next-auth/react";

export const ApiFlora=async()=> {
  const { data: session } = useSession();
  const user = session?.user;

  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${user?.token}`,
    },
  };
  const response = await fetch(
    `http://fastapi:80/api/rescue_flora`,
    requestOptions
  );
  const data = await response.json();
  return data;
}

