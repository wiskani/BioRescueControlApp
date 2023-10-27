import NextAuth from "next-auth";

declare module "next-auth" {
    interface Session {
        user: {
            id: number;
            name: string;
            email: string;
            last_name: string;
            permissions: string[];
            token: string;
        };
    }
}
