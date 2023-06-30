import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import type { NextAuthOptions } from 'next-auth'

export const authOptions: NextAuthOptions={
    // Configure one or more authentication providers
    providers: [
        CredentialsProvider({
            name: 'Credentials',
            credentials: {
                username: { label: "username", type: "text", placeholder: "correo electrónico" },
                password: { label: "aPssword", type: "password" }
            },
            async authorize(credentials, req) {
                const requestOptions = {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: JSON.stringify(
                        `grant_type=&username=${credentials?.username}&password=${credentials?.password}&scope=&client_id=&client_secret=`
                )}
                const res = await fetch("http://localhost:8000/api/token", requestOptions)
                const user = await res.json()
                console.log(user)
                if (user) {
                    return user 
                } else{
                    return null
                }
            }
        })
    ],
    callbacks: {
        async jwt({token, user}) {
            return { ...token, ...user}
        },
        async session({session, token, user}) {
            session.user = token as any;
            return session
        }
    },
}
