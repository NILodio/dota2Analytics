import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from "@chakra-ui/react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { useMutation, useQueryClient } from "@tanstack/react-query"

import { type ApiError, type PollCreate, PollsService } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"

interface AddPollProps {
  isOpen: boolean
  onClose: () => void
}

const AddPoll = ({ isOpen, onClose }: AddPollProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<PollCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      hero_id: 0,
      hero_name: "",
      team: "",
      player_name: "",
      description: "",
    },
  })
  const mutation = useMutation({
    mutationFn: (data: PollCreate) =>
      PollsService.createPoll({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "Poll created successfully.", "success")
      reset()
      onClose()
    },
    onError: (err: ApiError) => {
      const errDetail = (err.body as any)?.detail
      showToast("Something went wrong.", `${errDetail}`, "error")
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["polls"] })
    },
  })

  const onSubmit: SubmitHandler<PollCreate> = (data) => {
    mutation.mutate(data)
  }

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>Add Poll</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.hero_id}>
              <FormLabel htmlFor="Heri Id">Hero ID</FormLabel>
              <Input
                id="hero_id"
                {...register("hero_id", {
                  required: "Hero Id is required.",
                  pattern: {
                    value: /^[0-9]*$/,
                    message: "Hero Id should be a number.",
                  },
                })}
                placeholder="Hero Id"
                type="number"
              />
              {errors.hero_id && (
                <FormErrorMessage>{errors.hero_id.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl isRequired isInvalid={!!errors.hero_name}>
              <FormLabel htmlFor="hero_name">Hero Name</FormLabel>
              <Input
                id="hero_name"
                {...register("hero_name", {
                  required: "Hero Name is required.",
                })}
                placeholder="Hero Name"
                type="text"
              />
              {errors.hero_name && (
                <FormErrorMessage>{errors.hero_name.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl isRequired isInvalid={!!errors.team}>
              <FormLabel htmlFor="team">Team</FormLabel>
              <Input
                id="team"
                {...register("team", {
                  required: "Team is required.",
                })}
                placeholder="Team"
                type="text"
              />
              {errors.team && (
                <FormErrorMessage>{errors.team.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl mt={4}>
              <FormLabel htmlFor="player_name">Player Name</FormLabel>
              <Input
                id="player_name"
                {...register("player_name")}
                placeholder="Player Name"
                type="text"
              />
            </FormControl>
            <FormControl mt={4}>
              <FormLabel htmlFor="description">Description</FormLabel>
              <Input
                id="description"
                {...register("description")}
                placeholder="Description"
                type="text"
              />
            </FormControl>
          </ModalBody>

          <ModalFooter gap={3}>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default AddPoll
