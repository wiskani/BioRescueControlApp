import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
export default NextAuth({
    // Configure one or more authentication providers
    providers: [
        CredentialsProvider({
            name: 'Credentials',
            credentials: {
                email: { label: "Email", type: "text", placeholder: "correo electrónico" },
                password: { label: "Password", type: "password" }
            },
            async authorize(credentials, req) {
                const requestOptions = {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: JSON.stringify(
                        `grant_type=&username=${credentials.email}&password=${credentials.password}&scope=&client_id=&client_secret=`
                )}
                const res = await fetch("/api/token", requestOptions)
                const data = await res.json()
                if (res.ok && data.user) {
                    return data
                }
                return null
            }
        })
    ],
    callbacks: {
        async jwt(token, user) {
            return { ...token, ...user}
        },
        async session({session, token, user}) {
            session.user = token;
            return session
        }
    },
})
