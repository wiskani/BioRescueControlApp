import { useSession } from "next-auth/react";

export default function ApiFlora() {
  const { data: session } = useSession();


  return (
    <div>
      <h1>Api Flora</h1>
      <p>
        {status === "authenticated"
          ? `Signed in as ${session.user.email}`
          : "Not signed in"}
      </p>
    </div>
  );
}

