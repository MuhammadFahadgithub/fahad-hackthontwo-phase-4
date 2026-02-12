// page.tsx
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Welcome to Todo App</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <Button asChild>
            <Link href="/signup">Sign Up</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/login">Log In</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

