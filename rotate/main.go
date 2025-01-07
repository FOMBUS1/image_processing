package main

import (
	"bufio"
	"bytes"
	"image"
	"image/color"
	"image/jpeg"
	"image/png"
	"log"
	"strconv"
	"strings"

	"github.com/disintegration/imaging"
	"github.com/gofiber/fiber/v2"
)

type Message struct {
	Message string
}

func main() {
	app := fiber.New()

	img_channel := make(chan *image.NRGBA)

	app.Get("/", func(c *fiber.Ctx) error {
		log.Printf("IP request: %s", c.IP())
		return c.SendString("To rotate your image you need to send it to '/rotate'")
	})

	app.Post("/rotate", func(c *fiber.Ctx) error {
		log.Printf("IP request: %s", c.IP())

		file, err := c.FormFile("image")

		if err != nil {
			log.Println(err)
			return c.JSON(Message{Message: "Failed to recieve file"})
		}
		log.Printf("File is successfully recieved! Filename = %s", file.Filename)

		angle, err := strconv.ParseFloat(c.FormValue("angle"), 64)
		if err != nil {
			log.Println(err)
			return c.JSON(Message{Message: "Failed to get angle!"})
		}
		log.Printf("angle = %v", angle)

		img, err := file.Open()
		if err != nil {
			log.Println(err)
			return c.JSON(Message{Message: "Failed to open file"})
		}
		img_format := strings.Split(file.Filename, ".")[1]
		var decoded_img image.Image
		switch img_format {
		case "jpg":
			decoded_img, err = jpeg.Decode(img)
		case "jpeg":
			decoded_img, err = jpeg.Decode(img)
		case "png":
			decoded_img, err = png.Decode(img)
		default:
			log.Printf("Wrong format! Format = %s", img_format)
			return c.JSON(Message{Message: "Failed to decode image. Wrong format!"})
		}
		if err != nil {
			log.Println(err)
			return c.JSON(Message{Message: "Failed to decode image"})
		}
		log.Println("Image successfully decoded!")
		go rotate_img(decoded_img, angle, img_channel)
		log.Println("Image successfully rotated!")
		rotated_img := <-img_channel

		var imgBytes bytes.Buffer
		imgWriter := bufio.NewWriter(&imgBytes)
		png.Encode(imgWriter, rotated_img)

		return c.Send(imgBytes.Bytes())
	})

	log.Fatal(app.Listen("0.0.0.0:3000"))
}

func rotate_img(img image.Image, angle float64, img_channel chan *image.NRGBA) {
	rotated_img := imaging.Rotate(img, angle, color.RGBA{})
	img_channel <- rotated_img
}
