"use server";

export async function callAPI(wallState) {
  console.log("Calling API");
  try {
    // Fetch data from external API
    // const res = await fetch("http://localhost:5000/calculate_paint", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({ nosWalls: wallState }),
    // });
    const res = await fetch("http://localhost:5000/calculate_paint");

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const repo = await res.json();
    // Pass data to the page via props
    return repo;
  } catch (error) {
    console.error("Error calculating paint:", error);
  }
}
