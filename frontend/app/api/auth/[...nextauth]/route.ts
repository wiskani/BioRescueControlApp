import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'

const handler = NextAuth({
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
                const res = await fetch("http://127.0.0.1:8000/api/token", requestOptions)
                const data = await res.json()
                const token=data.access_token
                const requestOptions2 = {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: "Bearer " + token
                    },
                };
                const res2 = await fetch("http://127.0.0.1:8000/api/users/me", requestOptions2)
                const data_user = await res2.json()
                if (token && data_user) {
                    const user = {
                        ...data_user,
                        token: token
                    }
                    return user 
                } else{
                    return null
                }
            }
        })
    ],
    // Callbacks are asynchronous functions for session token and data user
    callbacks: {
        async jwt({token, user}) {
            return { ...token, ...user}
        },
        async session({session, token, user}) {
            session.user = token as any;
            
            return session
        }
    },
})

export { handler as GET, handler as POST } ;
